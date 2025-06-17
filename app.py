from flask import Flask, render_template, request, redirect, jsonify
from mysql import connector


app = Flask(__name__)


# Rotas do site

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/cadastro')
def cadastrar():
    return render_template('form.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/aulas')
def aulas():
    return render_template('aulas.html')



# cadastro

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':

        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')

        dados = (
            nome, email, telefone, senha
        )

        # conectando com mysql

        connect = connector.connect(
            host="localhost",
            database="KScadastro",
            user="root",
            password="horadeferrar"
        )

        cursor = connect.cursor()

        query = """
                INSERT INTO usuarios (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)
            """
        # executar o query e armazenar os dados

        cursor.execute(query, dados)

        connect.commit()

        # fechar a conexão com o banco de dados
        cursor.close()
        connect.close()

        return redirect('/')

    return render_template('form.html')


if __name__ == ('__main__'):
    app.run(debug=True)
