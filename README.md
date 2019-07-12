# pylint_flask_sqlalchemy

**Beware: this is still a WIP.**

## About

pylint_flask_sqlalchemy is [Pylint](https://www.pylint.org/) plugin for improving code
analysis when editing code using
[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com).

## Usage

Using a simple flask app

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
```

Before pylint_flask_sqlalchemy :

```sh
pylint app.py
```

After :

```sh
pylint --load-plugins pylint_flask_sqlalchemy app.py
```


## Installation 

```
pip install pylint_flask_sqlalchemy
```

## Roadmap

* [ ] write tests
* [ ] silence too-few-public-methods for models