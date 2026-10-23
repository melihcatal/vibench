import os
from typing import Optional
from datadog import initialize, api

def get_datadog_client() -> api.Client:
    """Return a configured Datadog API client using env vars for authentication.

    Required env vars: DD_API_KEY, DD_APP_KEY (or DD_CLIENT_TOKEN).
    """
    api_key = os.getenv('DD_API_KEY')
    app_key = os.getenv('DD_APP_KEY')
    if not api_key or not app_key:
        raise RuntimeError('Missing Datadog credentials. Set DD_API_KEY and DD_APP_KEY.')
    opts = {'api_key': api_key, 'app_key': app_key}
    initialize(**opts)
    # Use the higher-level API client for logs operations
    return api.Client()
