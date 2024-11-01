from .definitions import ArgumentDefinition
from argpi import Arguments as argpi, ArgumentDescription

class Arguments:
    def __init__(self) -> None:
        self.arguments = argpi().__capture__()

        # add
        for long, short in ArgumentDefinition.__arguments__.items():
            self.arguments.__add__(long, ArgumentDescription().shorthand(short))
        
        # analyse
        self.arguments.__analyse__()
    
    @property
    def analyse_and_get(self) -> argpi:
        return self.arguments