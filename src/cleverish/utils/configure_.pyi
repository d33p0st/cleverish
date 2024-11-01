from .tomler_ import Tomler
from ..exceptions.configuration_exceptions import ConfigurationError
from typing import Dict, List
from os.path import join, dirname as directory_name_of, basename, exists

class _ConfigurationObjectives:
    """`Internal class for all configuration paths`"""

    def __init__(self, configuration_object: Tomler) -> None:
        """`Do Not Use This Class for personal use.`"""
        ...

    @property
    def get(self) -> None:
        """`Get the configuration from Tomler Object.`
        
        This property is automatically invoked upon __init__.
        If you are looking for a reload functionality, use `reload`
        property
        """
        ...
    
    @property
    def reload(self) -> None:
        """`Reload the TOML file and it's configuration.`"""
        ...
    
    @property
    def environment_name(self) -> str:
        """`The Env Name to use for this current project.`
        
        If not provided, by default takes the `cleverish.toml` enclosing
        directory name as env name.
        """
        ...
    
    @property
    def dependency_directory(self) -> str:
        """`The Directory where the dependency for this env will be stored.`
        
        If not given, `current_dir/deps` will be used as default
        """
        ...
    
    @property
    def get_requirements_automatically(self) -> bool:
        """`Whether to Take Arguments Automatically.`"""
        ...
    
    @property
    def requirements_list(self) -> List[Dict[str, str]]:
        """`The Requirements List and Versions`"""
        ...

class ConfigurationInterpreter:
    """`Configuration Interpreter`"""
    @staticmethod
    def interpret(tomler: Tomler) -> _ConfigurationObjectives:
        """`Interpret the Configurations using a Tomler Object`"""
        ...