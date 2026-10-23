import os
import json

# Azure Service Bus integration
CONN_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def get_client() -> Any:
    """Initialize and return an Azure Service Bus client using environment variable.
    The client can be used for topic/subscription operations.
    """
    from azure.servicebus import ServiceBusClient

    return ServiceBusClient.from_connection_string(CONN_STR)


# Helper to normalize payload to dict


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {}
