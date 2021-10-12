# pylint_flask_sqlalchemy

[![Downloads](https://pepy.tech/badge/pylint-flask-sqlalchemy/month)](https://pepy.tech/project/pylint-flask-sqlalchemy)
[![Workflow](https://github.com/anybox/pylint_flask_sqlalchemy/actions/workflows/main.yml/badge.svg)](https://github.com/anybox/pylint_flask_sqlalchemy/actions)
[![PyPI](https://badge.fury.io/py/pylint-flask-sqlalchemy.svg)](https://pypi.org/project/pylint-flask-sqlalchemy/)

## About

`pylint_flask_sqlalchemy` is a [Pylint](https://www.pylint.org/) to improve static code
analysis of [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) based
projects.

## Usage

Using a simple flask app:

```python
"""app.py"""
# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Group {self.name}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    group = db.relationship(Group)

    def __repr__(self):
        return f"<User {self.username}>"

user = User(username="test")
db.session.add(user)
db.session.commit()
```

Without the plugin: `pylint app.py`

```
app.py:11:9: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:11:19: E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)
app.py:12:11: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:12:21: E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)
app.py:19:9: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:19:19: E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)
app.py:20:15: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:20:25: E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)
app.py:21:12: E1101: Instance of 'SQLAlchemy' has no 'relationship' member (no-member)
app.py:28:0: E1101: Instance of 'scoped_session' has no 'add' member (no-member)
app.py:29:0: E1101: Instance of 'scoped_session' has no 'commit' member (no-member)

----------------------------------------------------------------------
Your code has been rated at -18.95/10 (previous run: 10.00/10, -28.95)
```

😓

With pylint_flask_sqlalchemy: `pylint --load-plugins pylint_flask_sqlalchemy app.py`

```sh
----------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: -13.08/10, +23.08)
```

🥳

## Installation 

```
pip install pylint_flask_sqlalchemy
```

and tell pylint to `--load-plugins pylint_flask_sqlalchemy`.
