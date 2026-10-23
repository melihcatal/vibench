from typing import Dict, Any
from invoke_platform_model import invoke_platform_model
from model_models import GenerationRequest


def collect_platform_metadata(request: GenerationRequest) -> Dict[str, Any]:
    result = invoke_platform_model(request)
    response_id = getattr(result.raw_response, "id", None)
    created = getattr(result.raw_response, "created", None)
    return {
        "text": result.text,
        "usage": result.usage,
        "resource": result.resource,
        "model": result.model,
        "provider": "azure_openai",
        "response_id": response_id,
        "created": created,
        "raw_response": result.raw_response,
    }
