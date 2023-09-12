from dataclasses import dataclass
from functools import reduce
from pathlib import Path
import re
from typing import Final, Self

from nocto.filters import FILTERS


VARIABLES_REGEX: Final = re.compile(r"(?<!#)#{([^}]+)}", re.MULTILINE)


def _apply_filter(value: str, filter_name: str) -> str:
    return FILTERS[filter_name](value)


@dataclass(frozen=True, slots=True)
class Variable:
    name: str
    filters: tuple[str, ...]

    def process(self, value: str) -> str:
        """
        Applies `self.filters` in succession on the `value`
        """
        return reduce(_apply_filter, self.filters, value)

    @classmethod
    def from_string(cls, variable: str) -> Self:
        """
        Processes variables with filters - e.g. `Octopus.Release.Numbeer | VersionMajor`
        Into Variable(name='Octopus.Release.Number', filters=['VersionMajor'])
        """
        name, *filters = variable.split("|")
        return cls(name.strip(), tuple(filter_.strip() for filter_ in filters))


def find_variables(file: Path) -> frozenset[Variable]:
    with file.open() as f:
        return frozenset(Variable.from_string(variable) for variable in VARIABLES_REGEX.findall(f.read()))


def replace_variables(file: Path, variable_values: dict[Variable, str]) -> str:
    def replace(match: re.Match) -> str:
        variable = Variable.from_string(match.group(1))
        return variable_values[variable]

    with file.open() as f:
        return VARIABLES_REGEX.sub(replace, f.read())
