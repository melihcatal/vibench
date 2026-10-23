# [HELPER] model_client.py

import json
import os

from model_models import ManagedModelRequest


def load_config() -> dict:
    """Load platform configuration from environment variables or a config file.

    Returns a dict with provider‑specific settings.
    In a real project you would read a YAML/JSON config file and fall back to env vars.
    """
    config = {}
    # Example for Vertex AI: service account JSON path
    config["project_id"] = os.getenv("VERTEX_PROJECT_ID", "YOUR_PROJECT_ID")
    config["deployment_id"] = os.getenv("VERTEX_DEPLOYMENT_ID", "YOUR_DEPLOYMENT_ID")
    config["service_account_json"] = os.getenv(
        "VERTEX_SERVICE_ACCOUNT_JSON", "./vertex_ai_service_account.json"
    )
    return config


def build_platform_model(client, deployment_id: str, payload: dict) -> dict:
    """Invoke the managed model using the passed client object.

    Returns the raw API response dict.
    """
    try:
        response = client.generate_content(payload)
        return response
    except Exception as exc:
        raise RuntimeError(f"Failed to invoke model: {exc}")
