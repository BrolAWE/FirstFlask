from datetime import datetime

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config.from_object(config('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *
bootstrap = Bootstrap(app)
moment = Moment(app)


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


if __name__ == '__main__':
    app.run()
