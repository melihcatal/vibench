import os
from typing import Dict


def get_provider_config(provider: str) -> Dict[str, str]:
    configs = {
        "aws": {"region_name": os.getenv("AWS_REGION", "us-east-1")},
        "azure": {"vault_url": os.getenv("AZURE_KEY_VAULT_URL")},
        "google": {"project_id": os.getenv("GOOGLE_CLOUD_PROJECT")},
        "doppler": {
            "token": os.getenv("DOPPLER_TOKEN"),
            "config": os.getenv("DOPPLER_CONFIG", "dev"),
        },
    }
    return configs.get(provider, {})
