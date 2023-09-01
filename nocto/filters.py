from collections.abc import Callable
from typing import TypeAlias


Filter: TypeAlias = Callable[[str], str]


def _version_major(version: str) -> str:
    return version.split(".")[0]


def _version_minor(version: str) -> str:
    return version.split(".")[1]


def _version_patch(version: str) -> str:
    return version.split(".")[2]


FILTERS: dict[str, Filter] = {
    "VersionMajor": _version_major,
    "VersionMinor": _version_minor,
    "VersionPatch": _version_patch,
}
