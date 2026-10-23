# [SAME-SCENARIO] invoke_platform_model.py

from model_client import load_config, build_platform_model
from model_models import ManagedModelRequest, ManagedModelResponse


def invoke_platform_model(config, model_request: ManagedModelRequest):
    """Invokes a provider‑managed model through a platform client.

    Uses the helper utilities from `model_client` to load credentials and
    construct the request payload. Returns a `ManagedModelResponse` filled
    with the raw API payload and any platform‑specific metadata.

    Args:
        config (dict): Provider‑specific configuration (project, deployment,
                        credentials, etc.).
        model_request (ManagedModelRequest): Normalized request payload.

    Returns:
        ManagedModelResponse: Wrapped response with normalized fields and metadata.
    """
    # Load provider‑specific credentials / endpoint from env or config file
    platform_cfg = load_config()
    # Choose a concrete provider – Vertex AI (Google Cloud) in this example
    from vertexai.preview.language_models import TextGenerationModel  # type: ignore

    # Initialize the platform client based on the selected service
    client = TextGenerationModel.from_pretrained(model="gemma-2b")
    client.project = platform_cfg.get("project_id")
    client.location = "us-central1"

    # Build the raw request payload expected by the provider SDK
    payload = {
        "contents": [model_request.user_message],
        "parameters": {
            "max_output_tokens": model_request.max_tokens,
            "temperature": model_request.temperature,
        },
    }

    # Invoke the model and capture the raw response
    raw_response = build_platform_model(client, model_request.deployment_id, payload)

    # Construct a normalized response object
    return ManagedModelResponse(
        deployment_id=model_request.deployment_id,
        provider_payload=raw_response,
        metadata={
            "provider": "vertex-ai",
            "model_id": model_request.deployment_id,
            "request_id": raw_response.get("id"),
        },
    )
