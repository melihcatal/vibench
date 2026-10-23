# HELPER: observability_client.py
import os
from typing import Type

# Choose provider at runtime via environment variable
PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")

if PROVIDER == "datadog":
    from datadog import initialize, api

    def init_client() -> object:
        # Datadog client instance
        initialize(app_key=os.getenv("DD_APP_KEY"), api_key=os.getenv("DD_API_KEY"))
        return api.DatadogAPI()
else:
    # Generic placeholder for other providers; import real SDKs as needed
    class MetricsClient:
        @staticmethod
        def get():
            # Return a dummy client for illustration
            class Dummy:
                @staticmethod
                def query(*args, **kwargs):
                    return {"data": "dummy"}
            return Dummy()

MetricsClient.get_instance = init_client
