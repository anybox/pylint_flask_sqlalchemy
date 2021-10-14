"""Tests"""
import pytest
from pylint import epylint as lint

# pylint: disable=missing-docstring

E1 = ("E1101", "Instance of 'SQLAlchemy' has no 'Column' member")
E2 = ("E1101", "Instance of 'SQLAlchemy' has no 'Integer' member")
E3 = ("E1101", "Instance of 'SQLAlchemy' has no 'String' member")
E4 = ("E1101", "Instance of 'scoped_session' has no 'add' member")
E5 = ("E1101", "Instance of 'scoped_session' has no 'commit' member")


@pytest.mark.new
@pytest.mark.parametrize("with_plugin", [True, False])
@pytest.mark.parametrize(
    "filename, errors",
    [
        ("sqlalchemy_column", [E1, E2]),
        ("sqlalchemy_types", [E1, E2, E3]),
        ("scoped_session", [E4, E5]),
    ],
)
def test_plugin(with_plugin, filename, errors):
    args = [f"tests/data/{filename}.py"]
    if with_plugin:
        args.extend(["--load-plugins", "pylint_flask_sqlalchemy"])

    pylint_stdout, _ = lint.py_run(" ".join(args), return_std=True)
    err_messages = pylint_stdout.readlines()

    for error in errors:
        err_id, err_msg = error
        messages = [
            message for message in err_messages
            if err_id in message and err_msg in message
        ]
        assert bool(messages) != with_plugin
