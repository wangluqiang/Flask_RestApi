# coding=utf-8
from API import create_app, db
from API.models import User, Task
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
Migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
