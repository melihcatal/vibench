import os


def get_api_key(provider: str) -> str:
    env_var = f"{provider.replace('_', '').upper()}_API_KEY"
    key = os.getenv(env_var)
    if not key:
        raise ValueError(f"Missing environment variable {env_var}")
    return key
