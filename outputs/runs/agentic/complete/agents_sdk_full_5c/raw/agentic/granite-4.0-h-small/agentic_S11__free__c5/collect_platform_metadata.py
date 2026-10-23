import os
import json
from model_client import ManagedModelClient
from model_models import InvocationRequest, InvocationResponse

def collect_platform_metadata(prompt: str) -> dict:
    """
    Invoke a managed model and collect both the model output and provider platform metadata.
    Metadata may include usage stats, request ID, latency, and resource identifiers.
    """
    client = ManagedModelClient()
    request = InvocationRequest(model="gpt-4o-mini", deployment="default", prompt=prompt)
    # Placeholder for real provider call; here we simulate a response
    simulated_response = {
        "model_output": "The weather in Seattle is sunny today.",
        "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 9,
            "total_tokens": 21
        },
        "provider_metadata": {
            "request_id": "req-abc123",
            "latency_ms": 123,
            "model_id": "gpt-4o-mini",
            "deployment_id": "default"
        }
    }
    return simulated_response

if __name__ == "__main__":
    metadata = collect_platform_metadata("What's the weather like in Seattle?")
    print("Collected metadata:", json.dumps(metadata, indent=2))