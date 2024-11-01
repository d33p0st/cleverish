
from typing import List, Dict
from json import dump as dump_as_json, load as load_from_json

class DotLock:
    @staticmethod
    def create(dependencies: List[Dict[str, str]], name: str = 'clever') -> None:
        with open(name + '.lock', 'w+') as reference:
            dump_as_json(dependencies, reference, indent=4)
        
    @staticmethod
    def load(name: str = 'clever') -> List[Dict[str, str]]:
        with open(name + '.lock', 'r+') as reference:
            return load_from_json(reference)
    