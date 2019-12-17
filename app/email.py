from threading import Thread

from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        from app import mail
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    from manage import app
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = "Привет, Карина"
    msg.html = "Привет, привет"
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr