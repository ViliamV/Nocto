from itertools import chain
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated, Optional

from rich.console import Console
import typer

from nocto.environment import Environment
from nocto.filters import FILTERS
from nocto.types import VariableOverrides
from nocto.variables import Variable, find_variables, replace_variables


app = typer.Typer()
stdout_console = Console(color_system=None)
stderr_console = Console(stderr=True)
File = Annotated[
    Path,
    typer.Argument(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="File in which to replace variables",
    ),
]
DotenvFile = Annotated[
    Optional[Path],  # noqa: UP007 - typer has problems with X | Y
    typer.Option(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Optional .env file to use.",
    ),
]
Dotenv = Annotated[bool, typer.Option(help="Use dotenv to load .env file.")]
StdOut = Annotated[bool, typer.Option(help="Write output to stdout instead of temporary file.")]
Test = Annotated[
    bool, typer.Option(help="Only test if local environment has all required variables, don't replace variables.")
]
Vars = Annotated[
    Optional[list[str]],  # noqa: UP007 - typer has problems with X | Y
    typer.Option(help="Directly set variable value. E.g. FOO=BAR."),
]


def _process_variables_overrides(variables: Vars) -> VariableOverrides:
    if variables is None:
        return ()
    #                                                                       ↓ mypy does not understand maxsplit
    return tuple(tuple(var.split("=", maxsplit=1)) for var in variables)  # type: ignore[misc]


def _test_environment(environment: Environment, variables: frozenset[Variable]) -> None:
    """
    Tests if local `environment` has all the `variables`.
    """
    missing_variables = sorted({variable.name for variable in variables if variable.name not in environment})
    if missing_variables:
        stderr_console.print(
            f"Missing environment variable{'s' if len(missing_variables) > 1 else ''}: {missing_variables}"
        )
        raise typer.Exit(1)
    all_filters = chain.from_iterable(variable.filters for variable in variables)
    missing_filters = sorted({f for f in all_filters if f not in FILTERS})
    if missing_filters:
        stderr_console.print(f"Filter{'s' if len(missing_filters) > 1 else ''} not implemented: {missing_filters}")
        raise typer.Exit(1)


@app.command()
def replace(
    file: File,
    dotenv: Dotenv = True,
    dotenv_file: DotenvFile = None,
    var: Vars = None,
    stdout: StdOut = False,
    test: Test = False,
) -> None:
    """
    Replaces all Octopus-style template variables in `file` and writes it to temporary file.
    Returns path to temporary file.
    """
    variables = find_variables(file)
    variable_overrides = _process_variables_overrides(var)
    environment = Environment(dotenv, dotenv_file, variable_overrides)
    _test_environment(environment, variables)
    if test:
        return
    values = {variable: variable.process(environment[variable.name]) for variable in variables}
    output = replace_variables(file, values)
    if stdout:
        stdout_console.print(output)
    else:
        with NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(output)
            stdout_console.print(temp_file.name)


if __name__ == "__main__":
    app()  # pragma: no cover
