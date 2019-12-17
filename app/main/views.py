from datetime import datetime
from threading import Thread

from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from app.main.forms import NameForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config.from_object(config('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Alex]'
app.config['FLASKY_MAIL_SENDER'] = 'Alex <aleksejdelov@gmail.com>'
app.config['FLASKY_ADMIN'] = config('ALEX_ADMIN')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app.models import *


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = "Привет, Карина"
    msg.html = "Привет, привет"
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.ﬁlter_by(username=form.name.data).ﬁrst()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            db.session.commit()
            if True:
                send_email("aleksejdelov@gmail.com", 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
            db.session.commit()
        session['name'] = form.name.data
        db.session.commit()
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
