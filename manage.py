from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.middleware.profiler import ProfilerMiddleware

from app.main.views import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

@manager.command
def profile(length=25, profile_dir=None):
    """Запускает приложение в режиме профилирования кода."""
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()
