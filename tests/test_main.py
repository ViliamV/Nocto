from pathlib import Path

import pytest
from typer.testing import CliRunner

from nocto.main import app


RUNNER = CliRunner(mix_stderr=False)
HERE = Path(__file__).parent


@pytest.mark.parametrize(["input_name"], (("input_0.txt",), ("input_1.txt",)))
def test_test_command_no_changes(input_name: str) -> None:
    result = RUNNER.invoke(app, ["--test", str(HERE / "data" / input_name)])
    assert result.exit_code == 0
    assert result.stdout == ""


def test_test_command_input_2() -> None:
    # Missing
    result = RUNNER.invoke(app, ["--test", str(HERE / "data" / "input_2.txt"), "--no-dotenv"])
    assert result.exit_code == 1
    assert "Missing environment variables" in result.stderr

    # Passing dotenv (without all variables) - implicit
    result = RUNNER.invoke(app, ["--test", str(HERE / "data" / "input_2.txt")])
    assert result.exit_code == 1
    assert "Missing environment variables" in result.stderr
    assert "FOOBAR" not in result.stderr

    # Passing dotenv (with specified file)
    result = RUNNER.invoke(
        app, ["--test", str(HERE / "data" / "input_2.txt"), "--dotenv-file", str(HERE / "dotenv_test")]
    )
    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_missing_filter() -> None:
    result = RUNNER.invoke(
        app, ["--test", str(HERE / "data" / "input_3.txt"), "--dotenv-file", str(HERE / "dotenv_test")]
    )
    assert result.exit_code == 1
    assert "Filter not implemented" in result.stderr
    assert "ThisFilterIsNotImplementedYet" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize(
    ["input_name", "output_name"],
    (
        ("input_0.txt", "output_0.txt"),
        ("input_1.txt", "output_1.txt"),
        ("input_2.txt", "output_2.txt"),
    ),
)
def test_replace_command(input_name: str, output_name: str) -> None:
    result = RUNNER.invoke(app, [str(HERE / "data" / input_name), "--dotenv-file", str(HERE / "dotenv_test")])
    assert result.exit_code == 0
    with open(result.stdout.strip(), "r") as result_f, (HERE / "data" / output_name).open("r") as expected:
        result_text = result_f.read()
        expected_text = expected.read()
        assert result_text == expected_text


def test_replace_command_override() -> None:
    result = RUNNER.invoke(
        app,
        [
            str(HERE / "data" / "input_2.txt"),
            "--dotenv-file",
            str(HERE / "dotenv_test"),
            "--var",
            "VERSION=100.200.300",
        ],
    )
    assert result.exit_code == 0
    with open(result.stdout.strip(), "r") as result_f, (HERE / "data" / "output_2_override.txt").open("r") as expected:
        result_text = result_f.read()
        expected_text = expected.read()
        assert result_text == expected_text


def test_stdout() -> None:
    result = RUNNER.invoke(
        app,
        [
            str(HERE / "data" / "input_2.txt"),
            "--dotenv",
            "--dotenv-file",
            str(HERE / "dotenv_test"),
            "--stdout",
        ],
    )
    assert result.exit_code == 0
    with (HERE / "data" / "output_2.txt").open("r") as expected:
        # stdout contains 1 extra newline
        result_text = result.stdout[:-1]
        expected_text = expected.read()
        assert result_text == expected_text
