from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configurações do banco MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Freddydev@2025",
    "database": "cadastro"
}

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']

    conexao = None
    cursor = None

    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)",
            (nome, email, telefone, senha)
        )
        conexao.commit()
        return "Cadastro realizado com sucesso!"
    except mysql.connector.Error as erro:
        return f"Erro ao cadastrar: {erro}"
    finally:
     if cursor:
        cursor.close()
     if conexao:
        conexao.close()


if __name__ == '__main__':
    app.run(debug=True)
