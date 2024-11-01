from os import (
    listdir,
    getcwd,
    makedirs,
    name as osname,
    environ,
    geteuid,
    unlink,
    system as run,
    popen as get_output_of
)
from os.path import join, basename, exists, dirname
from typing import Union, Tuple, List, Dict
from colorama import Fore as _
from pathlib import Path
from packaging import version
from packaging.specifiers import SpecifierSet, InvalidSpecifier
import subprocess, sys, venv, ctypes, requests

from .exceptions import NonEmptyDirectory
from .utils import Tomler, ConfigurationInterpreter, TerminalEmulator
from .utils.dotlock import DotLock

class _ConstantTextContents:
    HELP: str
    PYPROJECT_TOML: str
    DEMO_CLEVERISH_TOML: str

class _DriverMethods:
    @staticmethod
    def create_init_file_at(location: str) -> None:
        """create a `__init__.py` file at a specified location."""
        ...
    
    @staticmethod
    def create_pyproject_toml_at(location: str, name: str) -> None:
        """create initial `pyproject.toml` file at the given location with the given package name."""
        ...
    
    @staticmethod
    def create_cleverish_toml_at(location: str) -> None:
        """create a `cleverish.toml` at the specified location."""
        ...

class DriverConfiguration:
    """`Class to store all driver configurations`"""
    def __init__(self) -> None:
        """`Create a driver configuration object`"""
        ...
    
    def set_force(self, value: bool) -> None:
        """sets force to a given value"""
        ...
    
    def set_package_name(self, value: str) -> None:
        """sets package name to a given value"""
        ...
    
    def set_package_status(self, value: bool) -> None:
        """sets package status to given value."""
        ...
    
    def set_tomler(self, value: Tomler) -> None:
        """sets tomler"""
        ...
    
    def set_to_add(self, value: Union[str, List[str], None]) -> None:
        """sets new package to add."""
        ...
    
    def set_upload_directory(self, value: Union[str, None]) -> None:
        """sets the upload directory to be uploaded."""
        ...
    
    @property
    def forceful_initialization(self) -> bool:
        """Force Init?"""
        ...
    
    @forceful_initialization.setter
    def forceful_initialization(self, force: bool) -> None: ...
    @forceful_initialization.deleter
    def forceful_initialization(self) -> None: ...

    @property
    def package_name(self) -> Union[str, None]:
        """`Package Name if any`"""
        ...
    
    @package_name.setter
    def package_name(self, name: Union[str, None]) -> None: ...
    @package_name.deleter
    def package_name(self) -> None: ...

    @property
    def package(self) -> bool:
        """`is it a package?`"""
        ...
    
    @package.setter
    def package(self, pkg: bool) -> None: ...
    @package.deleter
    def package(self) -> None: ...

    @property
    def tomler(self) -> Tomler:
        """`tomler if any`"""
        ...
    
    @tomler.setter
    def tomler(self, tomler: Tomler) -> None: ...
    @tomler.deleter
    def tomler(self) -> None: ...

    @property
    def to_add(self) -> Union[str, List[str], None]:
        """`to add new dependency if any.`"""
        ...
    
    @to_add.setter
    def to_add(self, value: Union[str, List[str], None]) -> None: ...
    @to_add.deleter
    def to_add(self) -> None: ...

    @property
    def upload_directory(self) -> Union[str, None]:
        """`the upload directory to look for uploading`"""
        ...

    @upload_directory.setter
    def upload_directory(self, value: Union[str, None]) -> None: ...
    @upload_directory.deleter
    def upload_directory(self) -> None: ...

class Drivers:
    """`Contains Drivers for all operations in cleverish domain.`"""
    @staticmethod
    def has_admin_priviledge() -> bool:
        """`Checks if the current session is root.`"""
        ...
    
    @staticmethod
    def relaunch_with_admin_priviledge() -> None:
        """`Relaunch session with admin priviledge`"""
        ...
    
    @staticmethod
    def clever_toml() -> bool:
        """`checks if clever.toml is present`"""
        ...
    
    @staticmethod
    def help() -> None:
        """`Prints Help`"""
        ...
    
    @staticmethod
    def init(config: DriverConfiguration) -> None:
        """`Initialize a new project.`"""
        ...
    
    @staticmethod
    def create_environment(config: DriverConfiguration) -> None:
        """`create environment`"""
        ...
    
    @staticmethod
    def shell(config: DriverConfiguration) -> None:
        """`run shell.`"""
        ...
    
    @staticmethod
    def get_all_versions(name: str) -> List[str]:
        """`get all versions of a package from pypi.`"""
        ...
    
    @staticmethod
    def get_latest_compatible_version(name: str, constraint: str) -> Union[str, None]:
        """from a list of globally available versions in pypi, get the compatible one if any using the constrain. else None."""
        ...

    @staticmethod
    def resolve_dependencies(dependencies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """resolve a list of dependencies based on manifest data."""
        ...
    
    @staticmethod
    def install_dependencies(config: DriverConfiguration, explicit: bool = True, extras: List[str] = [], user_given: List[str] = []) -> Tuple[int, int]:
        """`Install the dependencies.`"""
        ...
    
    @staticmethod
    def user_install_dependencies(config:DriverConfiguration) -> Tuple[int, int]:
        """for user installation"""
        ...
    
    @staticmethod
    def _strip(string: str) -> str:
        """`strip a string`"""
        ...
    
    @staticmethod
    def _find_required_dependencies(pip_path: Path, to_check: List[str]) -> List[str]:
        """`returns dependencies of the given to_check`"""
        ...

    @staticmethod
    def add(config: DriverConfiguration) -> None:
        """`Adds a dependency`"""
        ...
    
    @staticmethod
    def add_installation(name: str, version: Union[str, None], config: DriverConfiguration) -> bool:
        """`Installs a package. returns True upon success else False.`"""
        ...
    
    @staticmethod
    def build(config: DriverConfiguration) -> None:
        """`Builds the project.`"""
        ...
    
    @staticmethod
    def upload(config: DriverConfiguration) -> None:
        """`uploads to pypi`"""
        ...