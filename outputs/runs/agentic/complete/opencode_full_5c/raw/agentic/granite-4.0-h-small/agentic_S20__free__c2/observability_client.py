import os
import json


def get_log_service_url() -> str:
    """Return the managed log ingestion endpoint URL.

    Uses the provider-specific environment variable, e.g., DATADOG_API_URL.
    """
    return os.getenv("LOG_SERVICE_URL", "https://logs.example.com/api/v1/logs")


def get_translator_url() -> str:
    """Return URL for the translation endpoint of the provider (e.g., Azure Translator)."""
    return os.getenv("TRANSLATOR_URL", "https://api.example.com/translate")


def get_embedding_url() -> str:
    """Return URL for the embedding endpoint of the provider (e.g., OpenAI)."""
    return os.getenv("EMBEDDING_URL", "https://api.example.com/embeddings")


def get_auth_header() -> dict:
    """Construct the authentication header required by the provider.

    Most log services accept a bearer token from an env var like LOG_SERVICE_TOKEN.
    """
    token = os.getenv("LOG_SERVICE_AUTH_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def get_tracing_context() -> dict:
    """Helper to retrieve a tracing context (e.g., trace_id, span_id) if available."""
    # Example placeholders; in practice you'd retrieve from OpenTelemetry or framework.
    return {
        "trace_id": os.getenv("TRACE_ID", "default-trace"),
        "span_id": os.getenv("SPAN_ID", "default-span"),
    }
