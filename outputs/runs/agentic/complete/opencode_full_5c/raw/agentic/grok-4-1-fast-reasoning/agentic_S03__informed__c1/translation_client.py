import os
from typing import Dict, Any


def get_provider_config(provider: str) -> Dict[str, Any]:
    configs = {
        "deepl": {"auth_key": os.getenv("DEEPL_AUTH_KEY")},
        "google": {"credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")},
        "aws": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        },
        "azure": {
            "endpoint": os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
            "key": os.getenv("AZURE_TRANSLATOR_KEY"),
        },
    }
    return configs.get(provider, {})
