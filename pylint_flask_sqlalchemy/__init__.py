"""Pylint Flask SQLAlchemy plugin."""

from astroid import MANAGER, ClassDef, NodeNG
from pylint.lint import PyLinter

# flask-sqlalchemy wraps some sqlalchemy objects as its own
# see https://github.com/pallets/flask-sqlalchemy/blob/main/src/flask_sqlalchemy/__init__.py#L104
FLASK_SQLALCHEMY_WRAPS = [
    "relationship",
    "relation",
    "dynamic_loader",
]

VERSION = "1.0.0-pre"


def register(linter: PyLinter):
    """Plugin registration."""


def sort_module_keys(key: str):
    return -1 if key in FLASK_SQLALCHEMY_WRAPS else 1


def transform(node: NodeNG) -> NodeNG:
    """Make pylint understand FlaskSQLAlchemy proxies and wrappers.

    Note : it _looks_ like astroid transforms are run in some kind of try/except
    mechanism which makes some errors fail silently. For example, if you call:

    ```python
    from sqlalchemy.orm import Session
    Session.foo
    ```
    here, you would think it will raise an:
    `AttributeError: type object 'Session' has no attribute 'foo'`
    but... no. Instead it stops the transform and continue to the next node, so pylint
    does not raise an error, so you think your code (and ours) works, but it's not :-(
    So we need to write tests that fails to make sure our plugin works.
    """
    if node.name == "SQLAlchemy":
        import sqlalchemy
        import sqlalchemy.orm

        for module in sqlalchemy, sqlalchemy.orm:
            for key in sorted(module.__all__, key=sort_module_keys):
                if key not in FLASK_SQLALCHEMY_WRAPS:
                    node.locals[key] = [ClassDef(key, None)]
                else:
                    node.locals[key] = [
                        ClassDef(key, None),
                        node.locals["Query"]
                    ]
        return node
    if node.name == "scoped_session":
        from sqlalchemy.orm import Session

        for key in dir(Session):
            # `query` is in fact a proxy to `query_property`
            if key == "query":
                node.locals[key] = [ClassDef(key, None), node.locals["query_property"]]
            else:
                node.locals[key] = [ClassDef(key, None)]
        return node
    return node


MANAGER.register_transform(ClassDef, transform)
