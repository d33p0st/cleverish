class TomlDirectoryError(Exception):
    """`Toml Config directory error.`"""
    NOT_A_DIR: str

class TomlFileError(Exception):
    """`Toml file not found Error and related errors`"""
    FILE_NOT_FOUND: str
    NOT_A_FILE: str

class TomlerError(Exception):
    """`Generic Tomler Error`"""