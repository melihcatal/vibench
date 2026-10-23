from typing import Dict, Any
from model_client import WatsonXModelClient
from model_models import ModelResponse, normalize_response


def collect_platform_metadata(request: Dict[str, Any]) -> ModelResponse:
    """
    Invokes a watsonx.ai managed model and returns output with platform metadata.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """
    client = WatsonXModelClient(model_id="mistralai/mistral-large-latest")
    response = client.invoke(
        prompt=request.get("prompt", ""), parameters=request.get("parameters", {})
    )

    # Extract metadata from the response
    metadata = {
        "usage": {
            "input_tokens": response.get("results", [{}])[0]
            .get("usage", {})
            .get("input_tokens", 0),
            "output_tokens": response.get("results", [{}])[0]
            .get("usage", {})
            .get("output_tokens", 0),
        },
        "model_id": response.get("model_id"),
        "provider": response.get("provider"),
        "created_at": response.get("results", [{}])[0].get("created_at", ""),
    }

    response["metadata"] = metadata
    return normalize_response(response)
