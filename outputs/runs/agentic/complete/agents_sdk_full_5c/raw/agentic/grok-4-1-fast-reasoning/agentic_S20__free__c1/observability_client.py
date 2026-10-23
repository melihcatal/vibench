import os
from datadog_api_client import Configuration

def get_datadog_configuration() -> Configuration:
    """Get Datadog v2 API configuration from environment variables."""
    configuration = Configuration()
    configuration.api_key['apiKeyAuth'] = os.getenv('DD_API_KEY')
    configuration.api_key['appKeyAuth'] = os.getenv('DD_APP_KEY')
    site = os.getenv('DD_SITE', 'datadoghq.com')
    if site == 'datadoghq.eu':
        configuration.server_index = 3
    # default datadoghq.com server_index=None
    return configuration
