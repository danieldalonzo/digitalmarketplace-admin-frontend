#!/usr/bin/env python

import os
from app import create_app
from flask.ext.script import Manager, Server

application = create_app(
    os.getenv('DM_ADMIN_FRONTEND_ENVIRONMENT') or 'default'
)
manager = Manager(application)
manager.add_command("runserver", Server(port=5004))

if __name__ == '__main__':
    manager.run()
