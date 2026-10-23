import os
from typing import Any


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def openai_endpoint() -> str:
    return get_env("OPENAI_BASE_URL", "https://api.openai.com/v1")


def azure_service_bus_namespace() -> str:
    return get_env("AZURE_SERVICEBUS_NAMESPACE")


def openai_model() -> str:
    return get_env("OPENAI_MODEL", "gpt-5.4-mini")


def default_topic() -> str:
    return get_env("MESSAGE_TOPIC", "pubsub-events")


def default_subscription() -> str:
    return get_env("MESSAGE_SUBSCRIPTION", "pubsub-events-subscription")


def build_metadata(**values: Any) -> dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None}
