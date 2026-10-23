from __future__ import annotations

import os

from azure.servicebus import ServiceBusClient
from openai import OpenAI
from supabase import Client, create_client


def get_servicebus_connection_string() -> str:
    value = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not value:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING is required")
    return value


def get_servicebus_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(get_servicebus_connection_string())


def get_queue_name(default_env: str = "AZURE_SERVICEBUS_QUEUE_NAME") -> str:
    value = os.getenv(default_env)
    if not value:
        raise ValueError(f"{default_env} is required")
    return value


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def get_openai_model(default: str) -> str:
    return os.getenv("OPENAI_MODEL", default)


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    return create_client(url, key)


def get_supabase_table(default: str = "processed_messages") -> str:
    return os.getenv("SUPABASE_AUDIT_TABLE", default)
