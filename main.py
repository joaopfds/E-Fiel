from flask import Flask, jsonify, render_template, request, Request, request, logging
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:6e3bc464fcff*1ccD31-FG4c3cDE1GD3@viaduct.proxy.rlwy.net:18320/railway"
app.config['JSON_AS_ASCII'] = False
CORS(app)

db = SQLAlchemy(app)

class Usuario(db.Model):

    __tablename__='usuario'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)

    def __repr__(self):
        return f"usuario: {self.nome, self.email, self.senha}"

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def format_usuario(usuario):
        return {
            "nome": usuario.nome,
            "id" : usuario.id,
            "email": usuario.email,
            "senha" : usuario.senha
        }

class Empresa(db.Model):

    __tablename__='empresa'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)

    def __repr__(self):
        return f"empresa: {self.nome, self.email, self.senha, self.cnpj}"

    def __init__(self, nome, email, senha, cnpj):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cnpj = cnpj

    def format_empresa(empresa):
        return {
            "nome": empresa.nome,
            "id" : empresa.id,
            "email": empresa.email,
            "senha" : empresa.senha,
            "cnpj" : empresa.cnpj
        }

class Cartoes(db.Model):

    __tablename__='cartoes'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    validade = db.Column(db.Date)
    descricao = db.Column(db.String)
    pontos = db.Column(db.Integer)
    empresacnpj = db.Column(db.String)
    usuarioid = db.Column(db.Integer)

    def __repr__(self):
        return f"empresa: {self.validade, self.descricao, self.pontos, self.empresacnpj, self.usuarioid}"

    def __init__(self, validade, descricao, pontos, empresacnpj, usuarioid):
        self.validade = validade
        self.descricao = descricao
        self.pontos = pontos
        self.empresacnpj = empresacnpj
        self.usuarioid = usuarioid

    def format_cartoes(cartao):
        return {
            "validade": cartao.validade,
            "id" : cartao.id,
            "descricao": cartao.descricao,
            "pontos" : cartao.pontos,
            "empresacnpj" : cartao.empresacnpj,
            "usuarioid" : cartao.usuarioid
        }



@app.route('/usuarios')
def getUsuario():
    usuarios = Usuario.query.all()
    usuarios_list = []
    for usuario in usuarios:
        usuformatado = Usuario.format_usuario(usuario)
        usuarios_list.append(usuformatado)
        print(usuarios_list)
    return {"usuarios": usuarios_list}

@app.route('/insereusuario')
def postUsuario():
    usuario_Nome = request.json['nome']
    usuario_Email = request.json['email']
    usuario_Senha = request.json['senha']
    evento = Usuario(usuario_Nome, usuario_Email, usuario_Senha)
    db.session.add(evento)
    processo = db.session.commit()
    return {"processo" : processo}

@app.route('/empresas')
def getEmpresas():
    empresas = Empresa.query.all()
    empresas_list = []
    for empresa in empresas:
        formatado = Empresa.format_empresa(empresa)
        empresas_list.append(formatado)
        print(empresas_list)
    return {"empresas": empresas_list}

@app.route('/insereempresa')
def insereEmpresa():
    empresa_Nome = request.json['nome']
    empresa_Email = request.json['email']
    empresa_Senha = request.json['senha']
    empresa_cnpj = request.json['cnpj']
    evento = Empresa(empresa_Nome, empresa_Email, empresa_Senha, empresa_cnpj)
    db.session.add(evento)
    processo = db.session.commit()
    return {"processo" : processo}




@app.route('/cartoes')
def getCartoes():
    cartoes = Cartoes.query.all()
    cartoes_list = []
    for cartao in cartoes:
        formatado = Cartoes.format_cartoes(cartao)
        cartoes_list.append(formatado)
        print(cartoes_list)
    return {"cartoes": cartoes_list}

@app.route('/achacartao', methods = ['GET'])
def getCartao():
    data = request
    usuario_id = data.json['usuarioid']
    empresa_cnpj = data.json['empresacnpj']
    cartao = Cartoes.query.filter_by(usuarioid=usuario_id, empresacnpj = empresa_cnpj).first()
    formatado = Cartoes.format_cartoes(cartao)
    print(formatado)
    return {"cartao": formatado}

@app.route('/inserecartao')
def inserecartao():
    data = request
    cartao_validade = data.json['validade']
    cartao_descricao = data.json['descricao']
    cartao_pontos = data.json['pontos']
    cartao_empresacnpj = data.json['empresacnpj']
    cartao_usuarioid = data.json['usuarioid']
    evento = Cartao(cartao_validade, cartao_descricao, cartao_pontos, cartao_empresacnpj, cartao_usuarioid)
    db.session.add(evento)
    processo = db.session.commit()
    return {"processo" : processo}

@app.route('/ajustaponto', methods = ['GET'])
def ajustaponto():
    data = request
    usuario_id = data.json['usuarioid']
    empresa_cnpj = data.json['empresacnpj']
    cartao = Cartoes.query.filter_by(usuarioid = usuario_id, empresacnpj = empresa_cnpj).first()
    cartao.pontos = cartao.pontos + 1
    db.session.commit()
    cartao = Cartoes.query.filter_by(usuarioid = usuario_id, empresacnpj = empresa_cnpj).first()
    formatado = Cartoes.format_cartoes(cartao)
    print(formatado)
    return {"cartao": formatado}

@app.route('/deletaCartao')
def deletaCartao():
    data = request
    cartao_id = data.json['id']
    Cartoes.query.filter_by(id = cartao_id).delete()
    db.session.commit()
    cartao = Cartoes.query.filter_by(id = cartao_id).all()
    print(cartao)
    if (cartao is None) :
        return jsonify({"retorno":"deletado"})
    else:
        return jsonify({"retorno":"erro"})





@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅 xo xo"})


if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT", default=5000))


if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT", default=5000))