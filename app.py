import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imoveis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta onde as imagens serão armazenadas
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

# Definir as extensões permitidas
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)

# Modelo de dados para as residências
class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    imagem = db.Column(db.String(120), nullable=True)

with app.app_context():
    db.create_all()

# Função para analisar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query')  # Pega o termo da pesquisa, se existir
    if query:
        # Filtra os imóveis com base no nome ou bairro
        imoveis = Imovel.query.filter(
            Imovel.nome.ilike(f'%{query}%') | Imovel.bairro.ilike(f'%{query}%')
        ).all()
    else:
        # Se não houver pesquisa, pega todos os imóveis
        imoveis = Imovel.query.all()

    return render_template('index.html', imoveis=imoveis)


# Página para compartilhar residência (cadastro de imóveis)
@app.route('/compartilhar', methods=['GET', 'POST'])
def compartilhar():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        bairro = request.form['bairro']
        endereco = request.form['endereco']
        
        # Lidar com a imagem
        imagem = request.files['imagem']
        imagem_filename = None
        if imagem and allowed_file(imagem.filename):
            imagem_filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))

        # Cria um novo imóvel
        novo_imovel = Imovel(nome=nome, valor=valor, bairro=bairro, endereco=endereco, imagem=imagem_filename)
        
        # Adiciona ao banco de dados e faz o commit
        db.session.add(novo_imovel)
        db.session.commit()
        
        return redirect(url_for('index'))  # Redireciona para a página inicial
    
    return render_template('compartilhar.html')

if __name__ == '__main__':
    # Verifica se a pasta 'uploads' existe, senão cria
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
