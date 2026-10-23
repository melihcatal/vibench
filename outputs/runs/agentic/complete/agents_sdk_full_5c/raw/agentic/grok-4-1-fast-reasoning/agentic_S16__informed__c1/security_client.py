import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_provider_env(provider: str) -> Dict[str, str]:
    """Load environment variables for a specific secret provider."""
    env_maps = {
        'aws': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION'],
        'azure': ['AZURE_KEY_VAULT_URL'],
        'google': ['GOOGLE_CLOUD_PROJECT'],
        'ibm': ['IBM_SECRETS_MANAGER_APIKEY', 'IBM_SECRETS_MANAGER_URL']
    }
    config = {}
    vars_to_load = env_maps.get(provider, [])
    for var in vars_to_load:
        value = os.getenv(var)
        if value:
            config[var] = value
        else:
            logger.warning(f"Missing environment variable for {provider}: {var}")
    return config