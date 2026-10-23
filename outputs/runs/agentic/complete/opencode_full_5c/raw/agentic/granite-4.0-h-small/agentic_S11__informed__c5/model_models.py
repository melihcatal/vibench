# [HELPER] model_models.py

from typing import TypedDict


class ManagedModelRequest(TypedDict):
    """Normalized request payload for the workflow.

    Attributes:
        user_message (str): The natural‑language prompt or query.
        model_name (str): Human‑readable identifier (e.g., 'gemma-2b').
        deployment_id (str): Provider‑specific deployment/endpoint name.
        max_tokens (int): Max tokens to generate.
        temperature (float): Sampling temperature.
    """

    user_message: str
    model_name: str
    deployment_id: str
    max_tokens: int
    temperature: float


class ModelCatalogEntry(TypedDict):
    """Entry from a local model catalog (e.g., env var mapping or config file)."""

    provider: str  # e.g., 'vertex-ai', 'azure-openai'
    project_id: str
    deployment_id: str
    endpoint: str = ""
    api_key: str = ""


class ManagedModelResponse(TypedDict):
    """Normalized response object used throughout the workflow.

    Attributes:
        deployment_id (str): The identifier used for the call.
        provider_payload (dict): Raw dict returned by the provider SDK.
        metadata (dict): Provider‑specific details (usage, request_id, etc.).
    """

    deployment_id: str
    provider_payload: dict
    metadata: dict
