from flask_script import Manager
from flask_migrate import MigrateCommand

from app import app, db, migrate

manager = Manager(app)

# Add the 'db' command
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
