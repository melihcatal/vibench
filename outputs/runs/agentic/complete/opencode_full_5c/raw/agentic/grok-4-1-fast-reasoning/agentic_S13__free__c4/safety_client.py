import os


def get_api_key(env_var: str) -> str:
    value = os.getenv(env_var)
    if not value:
        raise ValueError(f"Environment variable {env_var} is not set.")
    return value
