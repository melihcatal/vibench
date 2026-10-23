from typing import Dict, Any
from model_client import WatsonXModelClient
from model_models import ModelRequest, normalize_request


def invoke_platform_model(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invokes a watsonx.ai managed model using the provided request.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """
    normalized_request = normalize_request(request)
    client = WatsonXModelClient(model_id="mistralai/mistral-large-latest")

    response = client.invoke(
        prompt=normalized_request.prompt, parameters=normalized_request.parameters
    )
    return response
