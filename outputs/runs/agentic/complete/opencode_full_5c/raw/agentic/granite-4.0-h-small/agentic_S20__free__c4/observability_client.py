import os
from typing import Any, Dict


def get_log_client(service_name: str) -> Any:
    """Factory for instantiating a concrete Managed Log service client.

    Supports only Datadog for demonstration; extend mapping for others.

    Args:
        service_name: Identifier string (e.g., "datadog").

    Returns:
        A configured client object with a `create_log` method.
    """
    if service_name == "datadog":
        # Placeholder: in real code you would import the Datadog SDK and configure it
        class DatadogClient:
            def create_log(self, payload: str) -> Dict[str, Any]:
                # Simulate sending log to Datadog HTTP API
                return {"status": "ok", "message": f"Log posted ({len(payload)} bytes)"}

        return DatadogClient()
    else:
        raise ValueError(f"Unsupported logging service: {service_name}")
