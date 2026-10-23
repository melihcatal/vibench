import os
from datadog import initialize, api


def init_datadog_client():
    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise ValueError(
            "DATADOG_API_KEY and DATADOG_APP_KEY environment variables must be set."
        )
    initialize(api_key=api_key, app_key=app_key)
