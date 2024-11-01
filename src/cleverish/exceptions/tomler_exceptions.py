class TomlDirectoryError(Exception):
    NOT_A_DIR = "NOT A DIRECTORY: {} (internal error)"

class TomlFileError(Exception):
    FILE_NOT_FOUND = "\'cleverish.toml\' or \'Cleverish.toml\' not found. Refer to official documentation for help."
    NOT_A_FILE = "{} is not a FILE."

class TomlerError(Exception):
    pass