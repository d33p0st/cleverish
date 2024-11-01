from .definitions import ArgumentDefinition
from argpi import Arguments as argpi, ArgumentDescription

class Arguments:
    """`Argument Parser`"""
    def __init__(self) -> None: ...
    @property
    def analyse_and_get(self) -> argpi: ...