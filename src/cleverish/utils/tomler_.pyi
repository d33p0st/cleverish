from toml import load as load_configuration, dump as dump_configuration
from typing import Any as AnyEntryData, Union as Either, List
from os.path import exists, isdir, isfile, join, expanduser, expandvars
from os import getcwd as current_working_directory

from ..exceptions.tomler_exceptions import TomlDirectoryError, TomlFileError, TomlerError

class Tomler:
    """`Tomler Class helps with Cleverish.Toml file for loading or saving configurations`"""
    
    def __init__(
            self,
            configuration_directory: str = current_working_directory(),
            configuration_name: List[str] = ['clever', 'Clever'],
        ) -> None:
        """`Tomler Object Creation`

        Raises TomlDirectoryError or TomlFileError based on check conditions.
        
        #### Parameter Description

        - `configuration_directory`: The Directory to look for configuration toml.
        - `configuration_name`: The eligible names for the configuration file.
        """
        ...
    
    @property
    def filepath(self) -> str:
        """`Returns the Toml FilePath`"""
        ...
    
    @property
    def load_configuration(self) -> None:
        """`Load Configuration From the Given Paramters in __init__.
        This property is automatically invoked in __init__.
        Use it to reload the Data.`"""
        ...
    
    @property
    def dump_configuration(self) -> None:
        """`Save The Configuration Data To The Configuration File.
        This property is automatically invoked in the internal functions while adding,
        changing or deleting entries. Use it to re-save it.`"""
        ...
    
    def add_or_modify_entry(self, root: str, value: AnyEntryData) -> None:
        """`Add or modify any entry.`
        
        Creates an entry if Not present.

        #### Parameter Description

        - `root`: The Key value to which data will be stored.

        For Example:

        Let us take the below written TOML Configuration as an example

        > [config]  
        > auto-detect = true

        To change this `auto-detect` value, use the following python code:

        ```
        >>> from cleverish.utils import Tomler
        >>> tomler = Tomler(...)
        >>> tomler.add_or_modify_entry(
        ...     root='config.auto-detect',
        ...     value=True
        ... )
        ```
        """
        ...
    
    def remove_entry(self, key: str, does_not_exists_ok: bool = False) -> None:
        """`Remove Any Entry`
        
        Raises `TomlerError` if `does_not_exists_ok` parameter is set to False, Default is False.

        For the following toml config:

        > [config]
        > auto-detect = true

        to remove `auto-detect`, use the following tomler code in python

        ```
        >>> from cleverish.utils import Tomler
        >>> tomler = Tomler(...)
        >>> tomler.remove_entry(
        ...     key='config.auto-detect'
        ... )
        ```
        """
        ...
    
    def fetch_entry(self, key: str) -> Either[AnyEntryData, None]:
        """`Fetch Any Key Value.`
        
        Returns `None` if key does not exist.
        """
        ...