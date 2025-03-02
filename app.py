import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///usuarios.db' 
app.config['SQLALCHEMY_BINDS'] = {
    'imoveis':'sqlite:///imoveis.db'
    } 
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)

class Imovel(db.Model):
    __bind_key__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    imagem = db.Column(db.String(120), nullable=True)

class Usuario(db.Model):
    nome = db.Column(db.String(120), primary_key=True)
    CPF = db.Column(db.Integer, nullable=False)
    contato = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120),nullable=False)

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query')
    if query:
        
        imoveis = Imovel.query.filter(
            Imovel.nome.ilike(f'%{query}%') | Imovel.bairro.ilike(f'%{query}%')
        ).all()
    else:
        
        imoveis = Imovel.query.all()

    return render_template('index.html', imoveis=imoveis)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        CPF = request.form['CPF']
        contato = request.form['contato']
        email = request.form['email']
        senha = request.form['senha']
    
        if Usuario.querry.filter_by(email = email):
            flash('O email já está cadastrado','danger')
            return redirect(url_for('cadastro'))
    
        novo_usuario = Usuario(nome=nome, CPF = CPF, contato = contato, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado!', 'success')
    return redirect(url_for('login'))

        


@app.route('/compartilhar', methods=['GET', 'POST'])
def compartilhar():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        bairro = request.form['bairro']
        endereco = request.form['endereco']
        
        
        imagem = request.files['imagem']
        imagem_filename = None
        if imagem and allowed_file(imagem.filename):
            imagem_filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))

    
        novo_imovel = Imovel(nome=nome, valor=valor, bairro=bairro, endereco=endereco, imagem=imagem_filename)
        
    
        db.session.add(novo_imovel)
        db.session.commit()
        
        return redirect(url_for('index')) 
    
    return render_template('compartilhar.html')

if __name__ == '__main__':

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
