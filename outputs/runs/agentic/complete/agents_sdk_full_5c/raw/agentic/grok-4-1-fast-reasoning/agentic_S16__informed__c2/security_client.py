import os
from typing import Dict, Any

def get_provider_config(provider: str) -> Dict[str, str]:
    configs = {
        "doppler": {"token": os.getenv("DOPPLER_TOKEN")},
        "google": {"project_id": os.getenv("GOOGLE_CLOUD_PROJECT")},
        "azure": {"vault_url": os.getenv("AZURE_KEY_VAULT_URL")},
        "aws": {"region": os.getenv("AWS_DEFAULT_REGION", "us-east-1")}
    }
    return configs.get(provider, {})