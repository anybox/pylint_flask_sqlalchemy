"""Tests"""
from pylint.lint import Run

# pylint: disable=missing-docstring

E1 = "tests/example.py:11:9: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)"
E2 = "tests/example.py:11:19: E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)"
E3 = "tests/example.py:12:25: E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)"
PARAMS = ["tests/example.py", "--errors-only", "--exit-zero"]


def test_without_plugin(capsys):
    try:
        Run(PARAMS)
    except SystemExit:
        pass
    captured = capsys.readouterr()
    returns = captured.out.split("\n")
    assert E1 in returns
    assert E2 in returns
    assert E3 in returns


def test_with_plugin(capsys):
    try:
        Run(
            [
                "tests/example.py",
                "--errors-only",
                "--exit-zero",
                "--load-plugins",
                "pylint_flask_sqlalchemy",
            ]
        )
    except SystemExit:
        pass
    captured = capsys.readouterr()
    returns = captured.out.split("\n")
    assert E1 not in returns
    assert E2 not in returns
    assert E3 not in returns
