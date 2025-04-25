from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import random

app = Flask(__name__)

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    email = request.form.get('email')

    if not email:
        return "E-mail inválido", 400

    # Gerar código aleatório de 6 dígitos
    codigo = str(random.randint(100000, 999999))

    corpo = f"""Olá! Recebemos sua solicitação de verificação.
Seu código de verificação é: {codigo}
Ele é válido por 10 minutos."""

    msg = MIMEText(corpo)
    msg['Subject'] = 'Código de Verificação'
    msg['From'] = 'seuemail@gmail.com'
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("seuemail@gmail.com", "senha_de_app_do_gmail")
        server.sendmail("seuemail@gmail.com", email, msg.as_string())
        server.quit()

        # Aqui seria legal armazenar o código no banco, com o e-mail do usuário e tempo de validade
        print(f"Código enviado para {email}: {codigo}")

        return "E-mail enviado com sucesso", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    app.run()
