import os
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse

SERVICE = "azure_openai"


def collect_platform_metadata(invocation_response: ModelInvocationResponse) -> dict:
    """
    Gather provider platform metadata alongside model output.
    For Azure OpenAI this includes:
      - usage details (token counts, model name)
      - resource identifier (deployment ID)
    """
    metadata = {
        "provider": SERVICE,
        "model": invocation_response.model,
        "deployment_id": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "usage": {
            "completion_tokens": invocation_response.usage.completion_tokens,
            "prompt_tokens": invocation_response.usage.prompt_tokens,
        },
    }
    return metadata
