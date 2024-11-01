from .add_analyse import Arguments
from typing import Callable, Any, Union, List
from argpi import FetchType

class PathWays:
    """`PathWay Formatter for Arguments`"""
    def __init__(self) -> None:
        """`Create a PathWay Object`"""
        ...
    
    def register(self, name: str, func: Callable, use_argument_value: bool = False, FetchType: FetchType = FetchType.SINGULAR, *args, **kwargs) -> Any:
        """`Register an Argument for execution`
        
        Returns whatever the function returns.
        """
        ...
    
    def fetch(self, name: str, fetchtype: FetchType) -> Union[str, List[str]]:
        """`Fetch value of an argument`"""
        ...