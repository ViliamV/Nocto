import os
from pathlib import Path

from dotenv import dotenv_values, find_dotenv

from nocto.types import VariableOverrides


class Environment:
    def __init__(self, use_dotenv: bool, dotenv_file: Path | None, variable_overrides: VariableOverrides) -> None:
        self._values: dict[str, str | None] = dict(os.environ)
        if use_dotenv:
            # Use cwd instead of this file's location
            # Also, help mypy understand the type
            dotenv_path: str | Path | None = dotenv_file if dotenv_file is not None else find_dotenv(usecwd=True)
            self._values |= dotenv_values(dotenv_path)
        self._values |= dict(variable_overrides)

    def __getitem__(self, key: str, /) -> str:
        value = self._values.get(key)
        if value is None:
            raise RuntimeError(f"This should never happen: variable {key!r} not set")
        return value

    def __contains__(self, key: str, /) -> bool:
        return key in self._values
