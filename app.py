# bibliotecas
from flask import Flask, render_template, request, redirect
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
import sqlite3
import os

app = Flask(__name__)

# Carregando email no backend
load_dotenv()
EMAIL_USUARIO = os.getenv('EMAIL_USUARIO')
EMAIL_SENHA = os.getenv('EMAIL_SENHA')


# Estruturação do email

def enviar_email(nome, email, telefone, matricula, classe, curso, disciplina):
    corpo = f"""
    Olá,

    Um novo usuário preencheu o formulário:

    Nome: {nome}
    Email: {email}
    Telefone: {telefone}
    Matricula: {matricula}
    Classe: {classe}
    Curso: {curso}
    Disciplina: {disciplina}

    Att,
    Backend do KS ACADEMY
    """

    msg = MIMEText(corpo)
    msg['Subject'] = 'Inscrição no KS ACADEMY!'
    msg['From'] = EMAIL_USUARIO
    # aqui selecionamos em quem o email será enviado, no caso nós próprios
    msg['To'] = EMAIL_USUARIO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USUARIO, EMAIL_SENHA)
            smtp.send_message(msg)
            print("Email enviado com sucesso.")
    except Exception as e:
        print("Erro ao enviar email:", e)

# Criação do banco


def criar_banco():
    if not os.path.exists("banco.db"):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone INTEGER NOT NULL,
                matricula TEXT NOT NULL,
                classe INTEGER NOT NULL,
                curso TEXT NOT NULL,
                disciplina TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/inscricao')
def form():
    return render_template('inscricao.html', mostrar_popup=False)


@app.route('/sobre')
def about():
    return render_template('sobre.html')


@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

# Rotas exercendo Funções :)


@app.route('/send', methods=['POST'])
def send():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    matricula = request.form['matricula']
    classe = request.form['classe']
    curso = request.form['curso']
    disciplina = request.form['disciplina']
    
    criar_banco()

    # Enviado dados para um banco de dados SQL

    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, telefone, matricula, classe, curso, disciplina) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nome, email, telefone, matricula,  classe, curso, disciplina))
        conn.commit()
        conn.close()

        print()
        print(f"Dados do {nome} salvos no banco.")
        print()
        confirm_data = True
    except Exception as e:
        print()
        print("Erro ao salvar dados no banco.", e)
        print()
        confirm_data = False

    if confirm_data == True:
        enviar_email(nome, email, telefone, matricula,
                     classe, curso, disciplina)

    return render_template('inscricao.html', mostrar_popup=True, nome=nome)


if __name__ == '__main__':
    app.run(debug=True)
