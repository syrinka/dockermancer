from inspect import getdoc
from typing import Callable

from autogen_core.tools import FunctionTool


def wraptool(func: Callable, name: str | None = None) -> FunctionTool:
    return FunctionTool(func, description=getdoc(func) or "No description", name=name)
