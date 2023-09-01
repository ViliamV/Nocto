from itertools import chain
from pathlib import Path
from typing import Annotated, Optional

from rich.console import Console
import typer

from nocto.env import get_env_variable, has_env_variable
from nocto.filters import FILTERS
from nocto.types import VariableOverrides
from nocto.variables import find_variables, replace_variables


app = typer.Typer()
stdout = Console()
stderr = Console(stderr=True)
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
        help="Optional .env file to use",
    ),
]
Dotenv = Annotated[bool, typer.Option(help="Use dotenv to load .env file")]
Vars = Annotated[
    Optional[list[str]],  # noqa: UP007 - typer has problems with X | Y
    typer.Option(help="Directly set variable value. E.g. FOO=BAR"),
]


def _process_variables_overrides(variables: Vars) -> VariableOverrides:
    if variables is None:
        return ()
    #                                                                       ↓ mypy does not understand maxsplit
    return tuple(tuple(var.split("=", maxsplit=1)) for var in variables)  # type: ignore[misc]


@app.command()
def test(file: File, dotenv: Dotenv = False, dotenv_file: DotenvFile = None, var: Vars = None) -> None:
    """
    Tests if local environment has all the variables required to replace Octopus-stype templated variables in `file`.
    """
    variables = find_variables(file)
    variable_overrides = _process_variables_overrides(var)
    missing_variables = sorted(
        {
            variable.name
            for variable in variables
            if not has_env_variable(variable.name, dotenv, dotenv_file, variable_overrides)
        }
    )
    if missing_variables:
        stderr.print(f"Missing environment variable{'s' if len(missing_variables) > 1 else ''}: {missing_variables}")
        raise typer.Exit(1)
    all_filters = chain.from_iterable(variable.filters for variable in variables)
    missing_filters = sorted({f for f in all_filters if f not in FILTERS})
    if missing_filters:
        stderr.print(f"Filter{'s' if len(missing_filters) > 1 else ''} not implemented: {missing_filters}")
        raise typer.Exit(1)


@app.command()
def replace(file: File, dotenv: Dotenv = False, dotenv_file: DotenvFile = None, var: Vars = None) -> None:
    """
    Replaces all Octopus-style template variables in `file` and writes it to temporary file.
    Returns path to temporary file.
    """
    test(file, dotenv, dotenv_file)
    variables = find_variables(file)
    variable_overrides = _process_variables_overrides(var)
    values = {
        variable: variable.process(get_env_variable(variable.name, dotenv, dotenv_file, variable_overrides))
        for variable in variables
    }
    output_path = replace_variables(file, values)
    stdout.print(output_path)


if __name__ == "__main__":
    app()
