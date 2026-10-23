import json
from typing import Dict, Any
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def collect_platform_metadata(
    deployment_id: str, prompt: str
) -> Dict[str, Any]:
    """
    Invokes a model and returns a dictionary containing both the model's
    textual output and platform-specific metadata (usage, request_id, model_handle, etc.).
    The metadata keys are provider‑specific but are normalized into a generic schema:
    {
        "output": "...",
        "metadata": {
            "request_id": "...",
            "model_handle": "...",
            "usage": {
                "input_tokens": 12,
                "output_tokens": 8,
                "price_usd": 0.0003
            }
        }
    }
    """
    client = ManagedModelClient.from_env()
    request = ModelInvocationRequest(
        deployment=deployment_id,
        prompt=prompt,
    )
    response: ModelInvocationResponse = client.invoke(request)
    # Gather output and metadata
    result = {
        "output": response.text,
        "metadata": {
            "request_id": getattr(response, "request_id", None),
            "model_handle": getattr(response, "model_handle", None),
            "usage": getattr(response, "usage", None),   # may be a dict from provider
        }
    }
    return result

# Command‑line helper (optional)
if __name__ == "__main__":
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("DEPLOYMENT_ID must be set.")
    prompt = "What is the capital of France?"
    data = collect_platform_metadata(deployment, prompt)
    print(json.dumps(data, indent=2))
