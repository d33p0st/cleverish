class NonEmptyDirectory(Exception):
    """`Directory Not Empty Exception`"""
    NOT_EMPTY: str

class CleverConfigurationNotFound(Exception):
    """`Clever dot toml missing Exception`"""
    INIT_FIRST: str