"""Pylint Flask SQLAlchemy plugin."""

from astroid import MANAGER, ClassDef
from pylint.lint import PyLinter

VERSION = "0.2.0"


def register(linter: PyLinter):
    """Plugin registration."""

def transform(cls) -> None:
    """Mimics Flask-SQLAlchemy's _include_sqlalchemy ."""
    if cls.name == "SQLAlchemy":
        import sqlalchemy
        import sqlalchemy.orm

        for module in sqlalchemy, sqlalchemy.orm:
            for key in module.__all__:
                cls.locals[key] = [ClassDef(key, None)]
    if cls.name == "scoped_session":
        from sqlalchemy.orm import Session

        for key in Session.public_methods:
            cls.locals[key] = [ClassDef(key, None)]

MANAGER.register_transform(ClassDef, transform)
