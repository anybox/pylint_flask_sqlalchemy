"""Tests"""
import pytest
from pylint.lint import Run

# pylint: disable=missing-docstring

E1 = "E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)"
E2 = "E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)"
E3 = "E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)"
E4 = "E1101: Instance of 'scoped_session' has no 'add' member (no-member)"
E5 = "E1101: Instance of 'scoped_session' has no 'commit' member (no-member)"
PARAMS = ["tests/example.py", "--errors-only", "--exit-zero"]


@pytest.mark.parametrize("with_plugin", [True, False])
@pytest.mark.parametrize("error", [E1, E2, E3, E4, E5])
def test_error(capsys, with_plugin, error):
    if with_plugin:
        PARAMS.extend(["--load-plugins", "pylint_flask_sqlalchemy"])
    try:
        Run(PARAMS)
    except SystemExit:
        pass
    captured = capsys.readouterr()
    for message in captured.out.split("\n"):
        assert error in message != with_plugin, captured.out
1