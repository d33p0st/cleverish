
from typing import List, Dict
from json import dump as dump_as_json, load as load_from_json

class DotLock:
    """`.lock Class`"""
    @staticmethod
    def create(dependencies: List[Dict[str, str]], name: str = 'clever') -> None:
        """`Create the .lock with given dependencies`"""
        ...
    
    @staticmethod
    def load(name: str = 'clever') -> List[Dict[str, str]]:
        """`Load the .lock file with given name.`"""
        ...