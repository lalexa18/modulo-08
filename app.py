from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from celery import Celery
from celery.py import make_celery
from app.models import initialize_database, Session, Article

# Configuración de Flask
app = Flask(__name__)
app.config.from_object("config.Config")

# Configuración de Flask-Mail
mail = Mail(app)

# Configuración de Celery
celery = make_celery(app)

# Ruta para enviar correos electrónicos
@app.route("/send_email", methods=["POST"])
def send_email():
    recipient = request.form.get("email")
    if not recipient:
        flash("Por favor, proporciona una dirección de correo válida.", "error")
        return render_template("index.html")

    # Enviar correo de forma asíncrona
    send_async_email.delay(recipient)
    flash("Correo enviado exitosamente.", "success")
    return render_template("index.html")

@celery.task
def send_async_email(recipient):
    """Enviar correo de manera asíncrona"""
    msg = Message(
        subject="Actualización de Presupuesto",
        sender=app.config["MAIL_USERNAME"],
        recipients=[recipient],
        body="¡Hola! Aquí está la actualización de tu presupuesto.",
    )
    with app.app_context():
        mail.send(msg)