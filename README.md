# pylint_flask_sqlalchemy

**Beware: this is still a WIP.**

## About

pylint_flask_sqlalchemy is [Pylint](https://www.pylint.org/) plugin for improving code
analysis when editing code using
[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com).

## Usage

Using a simple flask app

```python
"""app.py"""
# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

user = User(username="test")
db.session.add(user)
db.session.commit()
```

Without the plugin: `pylint app.py`

```
app.py:11:9: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:11:19: E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)
app.py:12:15: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
app.py:12:25: E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)
app.py:19:0: E1101: Instance of 'scoped_session' has no 'add' member (no-member)
app.py:20:0: E1101: Instance of 'scoped_session' has no 'commit' member (no-member)

----------------------------------------------------------------------
Your code has been rated at -13.08/10 (previous run: 10.00/10, -23.08)
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

and tell pylint to `--load-plugins pylint_flask_sqlalchemy` when you launch it. 
