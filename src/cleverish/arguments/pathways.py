from .add_analyse import Arguments
from typing import Callable, Any, Union, List
from argpi import FetchType

class PathWays:
    def __init__(self) -> None:
        self.arguments = Arguments().analyse_and_get
    
    def register(self, name: str, func: Callable, use_argument_value: bool = False, FetchType: FetchType = FetchType.SINGULAR, *args, **kwargs) -> Any:
        if self.arguments.__there__(name):
            if use_argument_value:
                return func(self.fetch(name, FetchType))
            else:
                return func(*args, **kwargs)
    
    def fetch(self, name: str, fetchtype: FetchType) -> Union[str, List[str]]:
        return self.arguments.__fetch__(name, fetchtype)