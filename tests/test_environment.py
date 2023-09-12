import pytest

from nocto.environment import Environment


def test_bare_environment() -> None:
    env = Environment(False, None, ())
    assert "PATH" in env
    assert "FOOBAR" not in env


def test_environment_with_dotenv() -> None:
    env = Environment(True, None, ())
    assert "FOOBAR" in env
    assert env["FOOBAR"] == "for-testing-only"


def test_environment_with_overrides() -> None:
    env = Environment(False, None, (("FOOBAR", "baz"),))
    assert "FOOBAR" in env
    assert env["FOOBAR"] == "baz"


def test_environment_raising() -> None:
    env = Environment(False, None, ())
    with pytest.raises(RuntimeError):
        env["FOOBAR"]
