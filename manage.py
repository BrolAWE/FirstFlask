from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from werkzeug.middleware.profiler import ProfilerMiddleware

from app import create_app, db
from app.models import User, Role

app = create_app("default")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


@manager.command
def profile(length=25, profile_dir=None):
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)

    app.run()
