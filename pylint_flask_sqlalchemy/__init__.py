"""
Pylint plugin
"""

from astroid import MANAGER, ClassDef

VERSION = "0.2.0"


def register(linter):  # pylint: disable=unused-argument
    """Plugin registration"""


def transform(cls):
    """
    Mimics Flask-SQLAlchemy's _include_sqlalchemy
    """
    if cls.name == "SQLAlchemy":
        import sqlalchemy  # pylint: disable=import-outside-toplevel
        import sqlalchemy.orm  # pylint: disable=import-outside-toplevel

        for module in sqlalchemy, sqlalchemy.orm:
            for key in module.__all__:
                cls.locals[key] = [ClassDef(key, None)]
    if cls.name == "scoped_session":
        from sqlalchemy.orm import Session  # pylint: disable=import-outside-toplevel

        for key in Session.public_methods:
            cls.locals[key] = [ClassDef(key, None)]


MANAGER.register_transform(ClassDef, transform)
