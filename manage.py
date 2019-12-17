from decouple import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.profiler import ProfilerMiddleware

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
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[25], profile_dir=None)
    app.run()
