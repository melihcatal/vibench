import os

def get_config_value(key: str, default: str = None) -> str:
    return os.getenv(key, default)

