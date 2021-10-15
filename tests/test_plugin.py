"""Tests Pylint Flask SQLAlchemy plugin."""
import pytest
from pylint import epylint as lint

E1 = ("E1101", "Instance of 'SQLAlchemy' has no 'Column' member")
E2 = ("E1101", "Instance of 'SQLAlchemy' has no 'Integer' member")
E3 = ("E1101", "Instance of 'SQLAlchemy' has no 'String' member")
E4 = ("E1101", "Instance of 'scoped_session' has no 'add' member")
E5 = ("E1101", "Instance of 'scoped_session' has no 'commit' member")
E6 = ("E1101", "Instance of 'relationship' has no 'filter' member")
E7 = ("E1101", "Instance of 'query' has no 'outerjoin' member")


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
            message
            for message in err_messages
            if err_id in message and err_msg in message
        ]
        assert bool(messages) != with_plugin


@pytest.mark.parametrize(
    "filename, errors",
    [("sqlalchemy_relationship", [E6, E7])],
)
def test_error_with_flask_sqlalchemy_wraps(filename, errors):
    """These tests raises errors only when using the plugin."""
    args = [
        f"tests/data/{filename}.py",
        "--load-plugins",
        "pylint_flask_sqlalchemy",
    ]
    pylint_stdout, _ = lint.py_run(" ".join(args), return_std=True)
    err_messages = pylint_stdout.readlines()

    for error in errors:
        err_id, err_msg = error
        messages = [
            message
            for message in err_messages
            if err_id in message and err_msg in message
        ]
        assert len(messages) == 0


@pytest.mark.parametrize("filename", ["scoped_session"])
def test_canary_scoped_session(filename):
    """Pylint *must* fail on these files or we broke something..."""
    args = [
        f"tests/canaries/{filename}.py",
        "--load-plugins",
        "pylint_flask_sqlalchemy",
    ]
    pylint_stdout, _ = lint.py_run(" ".join(args), return_std=True)
    assert "has no 'WHAT' member" in pylint_stdout.readlines()[-6]
