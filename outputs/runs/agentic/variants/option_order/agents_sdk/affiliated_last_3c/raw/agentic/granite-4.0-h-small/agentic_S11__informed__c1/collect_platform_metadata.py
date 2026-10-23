import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationMetadata

def collect_platform_metadata(resource_id: str, prompt: str) -> ModelInvocationMetadata:
    """
    Invoke a managed model and return both the textual output and provider platform metadata.
    Args:
        resource_id: Qualified model/deployment identifier.
        prompt: Input text.
    Returns:
        ModelInvocationMetadata containing output, usage stats, model handle, and request IDs.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(resource_id=resource_id, prompt=prompt)
    # Assume the client returns a richer response object with metadata
    full_response = client.invoke_model_full(request)
    return full_response.metadata

#
# Example usage (optional)
# if __name__ == "__main__":
#     rid = os.getenv("MODEL_RESOURCE_ID")
#     txt = os.getenv("USER_PROMPT", "What is the capital of France?\n")
#     meta = collect_platform_metadata(rid, txt)
#     print("Output:", meta.output)
#     print("Usage:", meta.usage)
#     print("Model handle:", meta.model_handle)
#     print("Request ID:", meta.request_id)
