import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = '1234'

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///usuarios.db' 
app.config['SQLALCHEMY_BINDS'] = {
    'imoveis':'sqlite:///imoveis.db'
    } 
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    CPF = db.Column(db.Integer, nullable=False)
    contato = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120),nullable=False)


class Imovel(db.Model):
    __tablename__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    imagem = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('imoveis', lazy=True))

#with app.app_context():
#    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/home', methods=['GET', 'POST'])
def index():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página', 'danger')
        return redirect(url_for('login'))
    
    query = request.args.get('query')
    if query:
        
        imoveis = Imovel.query.filter(
        Imovel.bairro.ilike(f'%{query}%') | Imovel.endereco.ilike(f'%{query}%')
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
    
        if Usuario.query.filter_by(email=email).first():
            flash('O email já está cadastrado','danger')
            return redirect(url_for('cadastro'))

    
        novo_usuario = Usuario(nome=nome, CPF = CPF, contato = contato, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado!', 'success')
    return redirect(url_for('login'))

        


@app.route('/compartilhar', methods=['GET', 'POST'])
def compartilhar():
    if request.method == 'POST':
        valor = request.form['valor']
        bairro = request.form['bairro']
        endereco = request.form['endereco']
        
        
        imagem = request.files['imagem']
        imagem_filename = None
        if imagem and allowed_file(imagem.filename):
            imagem_filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))

    
        usuario_id = session.get('usuario_id')

        novo_imovel = Imovel(
            valor=valor, 
            bairro=bairro, 
            endereco=endereco, 
            imagem=imagem_filename, 
            user_id=usuario_id
        )
        
    
        db.session.add(novo_imovel)
        db.session.commit()
        
        flash('Imovel compartilhado com sucesso!','sucess')
        return redirect(url_for('index')) 
    
    return render_template('compartilhar.html')

@app.route('/meus_imoveis')
def meus_imoveis():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        flash('Você precisa estar logado para acessar seus imóveis!', 'danger')
        return redirect(url_for('login'))
    
    imoveis = Imovel.query.filter_by(user_id=usuario_id).all()
    
    return render_template('meus_imoveis.html', imoveis=imoveis)

@app.route('/deletar_imovel/<int:id>', methods=['POST'])
def deletar_imovel(id):
    imovel = Imovel.query.filter_by(id=id, user_id=session.get('usuario_id')).first()
    
    if imovel:
        db.session.delete(imovel)
        db.session.commit()
        flash('Imóvel deletado com sucesso!', 'success')
    else:
        flash('Imóvel não encontrado ou você não tem permissão para deletá-lo.', 'danger')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
