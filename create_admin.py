from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input('Введите имя: ')

    if User.query.filter(User.username == username).count():
        print('Пользователь с таким именем уже существует!')
        sys.exit(0)
    
    pass1 = getpass('Введите пароль: ')
    pass2 = getpass('Повторите пароль: ')
    if not pass1 == pass2:
        print('Пароли отличаются!!!')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(pass1)

    db.session.add(new_user)
    db.session.commit()
    print('Пользователь с id {} успешно создан'.format(new_user.id))
