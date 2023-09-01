from collections.abc import Mapping
from functools import cache
import os
from pathlib import Path

from dotenv import dotenv_values

from nocto.types import VariableOverrides


@cache
def _env(dotenv: bool, dotenv_file: Path | None, variable_overrides: VariableOverrides) -> Mapping[str, str | None]:
    if not dotenv:
        return os.environ | dict(variable_overrides)
    return os.environ | dotenv_values(dotenv_file) | dict(variable_overrides)


def has_env_variable(name: str, dotenv: bool, dotenv_file: Path | None, variable_overrides: VariableOverrides) -> bool:
    return bool(_env(dotenv, dotenv_file, variable_overrides).get(name))


def get_env_variable(name: str, dotenv: bool, dotenv_file: Path | None, variable_overrides: VariableOverrides) -> str:
    value = _env(dotenv, dotenv_file, variable_overrides).get(name)
    if value is None:
        raise KeyError(f"Environment variable {name!r} not set")
    return value
