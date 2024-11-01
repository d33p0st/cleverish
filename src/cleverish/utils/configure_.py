
from .tomler_ import Tomler
from ..exceptions.configuration_exceptions import ConfigurationError
from typing import Dict, List
import os

class _ConfigurationObjectives:
    def __init__(self, configuration_object: Tomler) -> None:
        self.object = configuration_object
        self.get
    
    @property
    def get(self) -> None:
        # Try to get environment_name
        self._environment_name = self.object.fetch_entry('config.environment_name')

        if self._environment_name is None:
            self._environment_name = os.path.basename(os.path.dirname(self.object.filepath))
            self.object.add_or_modify_entry('config.environment_name', self.environment_name)
        
        if not isinstance(self._environment_name, str):
            raise ConfigurationError(f"Expected <class 'str'> for [config.environment_name], found: {type(self._environment_name)}")
        
        # Try to get dependency_directory
        self._dependency_directory = self.object.fetch_entry('requirements.dependency_directory')

        if self._dependency_directory is None:
            self._dependency_directory = os.path.join(os.path.dirname(self.object.filepath), 'deps')
            self.object.add_or_modify_entry('requirements.dependency_directory', self.dependency_directory)
        
        if not isinstance(self._dependency_directory, str):
            raise ConfigurationError(f"Expected <class 'str'> for [requirements.dependency_directory], found: {type(self._dependency_directory)}")
        
        # Try to get get-automatically
        self._requirements_auto = self.object.fetch_entry('requirements.get-automatically')

        if self._requirements_auto is None:
            self._requirements_auto = False
            self.object.add_or_modify_entry('requirements.get-automatically', self.get_requirements_automatically)
        
        if not isinstance(self._requirements_auto, bool):
            raise ConfigurationError(f"Expected <class 'bool'> for [requirements.get-automatically], found: {type(self._requirements_auto)}")
        
        # Try to get list of requirements
        self._requirements_list = self.object.fetch_entry('requirements.list')

        if self._requirements_list is None:
            self._requirements_list: List[Dict[str, str]] = []
            self.object.add_or_modify_entry('requirements.list', self.requirements_list)
        
        if not isinstance(self._requirements_list, list):
            raise ConfigurationError(f"Expected <class 'builtins.list'> for [requirements.list], found: {type(self._requirements_list)}")
    
    @property
    def reload(self) -> None:
        self.object.load_configuration
        self.get
    
    @property
    def environment_name(self) -> str:
        return self._environment_name

    @property
    def dependency_directory(self) -> str:
        return self._dependency_directory

    @property
    def get_requirements_automatically(self) -> bool:
        return self._requirements_auto
    
    @property
    def requirements_list(self) -> List[Dict[str, str]]:
        return self._requirements_list

class ConfigurationInterpreter:
    @staticmethod
    def interpret(tomler: Tomler) -> _ConfigurationObjectives:
        return _ConfigurationObjectives(tomler)
    