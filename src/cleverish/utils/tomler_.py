from toml import load as load_configuration, dump as dump_configuration
from typing import Any as AnyEntryData, Union as Either, List
from os.path import exists, isdir, isfile, join, expanduser, expandvars
from os import getcwd as current_working_directory

from ..exceptions.tomler_exceptions import TomlDirectoryError, TomlFileError, TomlerError

class Tomler:
    def __init__(self, configuration_directory: str = current_working_directory(), configuration_name: List[str] = ['clever', 'Clever']) -> None:
        self.configuration_directory = expanduser(expandvars(configuration_directory))

        if self.configuration_directory.startswith('./'):
            self.configuration_directory = join(current_working_directory(), self.configuration_directory[2:])
        
        if not isdir(self.configuration_directory):
            raise TomlDirectoryError(TomlDirectoryError.NOT_A_DIR.format(self.configuration_directory))
        
        Configuration_Check = False
        self.configuration_path = None

        for __configuration__ in configuration_name:
            self.configuration_path = join(self.configuration_directory, f'{__configuration__}.toml')

            if exists(self.configuration_path):
                Configuration_Check = True
            
            if not isfile(self.configuration_path):
                Configuration_Check = False
                self.configuration_path = None
            
            if Configuration_Check:
                break
        
        if self.configuration_path is None:
            raise TomlFileError(f"Couldn't Find Matching Configuration files: {configuration_name}")
        
        self.load_configuration
    
    @property
    def filepath(self) -> str:
        return self.configuration_path
    
    @property
    def load_configuration(self) -> None:
        with open(self.configuration_path, 'r+') as reference:
            self.configuration_data = load_configuration(reference)
    
    @property
    def dump_configuration(self) -> None:
        with open(self.configuration_path, 'w+') as reference:
            dump_configuration(self.configuration_data, reference)
    
    def add_or_modify_entry(self, root: str, value: AnyEntryData) -> None:
        keys = root.split('.')
        data = self.configuration_data

        # Traverse the keys except the last one, ensuring nested dictionaries are created
        for key in keys[:-1]:
            data = data.setdefault(key, {})
        
        data[keys[-1]] = value

        self.dump_configuration
    
    def remove_entry(self, key: str, does_not_exists_ok: bool = False) -> None:
        keys = key.split('.')
        data = self.configuration_data
        try:
            for k in keys[:-1]:
                data = data[k]
            
            del data[keys[-1]]
            self.dump_configuration
        except KeyError:
            if not does_not_exists_ok:
                raise TomlerError(f"Key removal failed for \'{key}\', Does not exist.")
    
    def fetch_entry(self, key: str) -> Either[AnyEntryData, None]:
        keys = key.split('.')
        data = self.configuration_data
        try:
            for k in keys:
                data = data[k]
            return data
        except KeyError:
            return None