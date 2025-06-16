#Importação de bibliotecas
from flask import Flask, render_template, request, redirect
import psycopg2


app = Flask(__name__)

# configuração do banco de dados

db_config = {
    "host":"localhost",
    "database":"cadastro",
    "user":"postgres",
    "password":"horadeferrar"
}


# Rotas do site

@app.route('/')
def cadastro():
    return render_template('form.html')


@app.route('/cadastrar', methods=['POST'])
def cadastro():
    nome = request.form('nome')
    email = request.form('email')
    telefone = request.form('telefone')
    senha = request.form('senha')


    try:
        conexao = psycopg2.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)",
            (nome, email, telefone, senha)
        )

        conexao.commit()
        cursor.close()
        conexao.close()
        return "Cadastro Realizado com sucesso!"
    
    except Exception as e:
        return f"Erro ao cadastrar: {e}"


# abrindo o site
if __name__ == '__main__':
    app.run(debug=True)