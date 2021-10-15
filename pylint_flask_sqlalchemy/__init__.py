"""Pylint Flask SQLAlchemy plugin."""

from astroid import MANAGER, ClassDef
from pylint.lint import PyLinter

# flask-sqlalchemy wraps some sqlalchemy objects as its own
# see https://github.com/pallets/flask-sqlalchemy/blob/main/src/flask_sqlalchemy/__init__.py#L104
FLASK_SQLALCHEMY_WRAPS = [
    "relationship",
    "relation",
    "dynamic_loader",
]

VERSION = "1.0.0"


def register(linter: PyLinter):
    """Plugin registration."""


def sort_module_keys(key: str):
    return -1 if key in FLASK_SQLALCHEMY_WRAPS else 1


def transform(cls) -> None:
    """Mimics Flask-SQLAlchemy's _include_sqlalchemy."""
    if cls.name == "SQLAlchemy":
        import sqlalchemy
        import sqlalchemy.orm

        for module in sqlalchemy, sqlalchemy.orm:
            for key in sorted(module.__all__, key=sort_module_keys):
                if key not in FLASK_SQLALCHEMY_WRAPS:
                    cls.locals[key] = [ClassDef(key, None)]
                else:
                    cls.locals[key] = [
                        ClassDef(key, None),
                        cls.locals["Query"]
                    ]

    if cls.name == "scoped_session":
        from sqlalchemy.orm import Session

        for key in Session.public_methods:
            cls.locals[key] = [ClassDef(key, None)]


MANAGER.register_transform(ClassDef, transform)
