#!/usr/bin/env python
import os
import sys
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from Config.PlatformPdo2 import PlatformPdo2

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    
    platformpdo2_obj = PlatformPdo2()
#     if platformpdo2_obj.OpenProject(app.config['BIM_PATH']):
#         print 'success to open project %s' % app.config['BIM_PATH']
#     else:
#         print 'fail to open project %s' % app.config['BIM_PATH']
#         sys.exit()
        
    manager.run()
