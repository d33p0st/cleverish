class NonEmptyDirectory(Exception):
    NOT_EMPTY = "{} directory is not empty."

class CleverConfigurationNotFound(Exception):
    INIT_FIRST = "Clever config (clever.toml) is not present in current directory, please run clever init."