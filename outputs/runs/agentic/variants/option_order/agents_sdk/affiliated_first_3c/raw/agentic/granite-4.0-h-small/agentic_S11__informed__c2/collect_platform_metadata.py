import json
from model_client import ManagedModelClient
from model_models import PromptRequest, PromptResponse


def collect_platform_metadata(prompt: str, max_tokens: int = 256) -> PromptResponse:
    """
    Invoke the model and return a PromptResponse that includes both the generated text
    and provider metadata such as model ID, request ID, usage details, and raw payload.
    """
    client = ManagedModelClient(provider="huggingface")
    request = PromptRequest(inputs=prompt, parameters={"max_new_tokens": max_tokens})
    response = client.invoke(request)
    # Build a richer local representation containing metadata
    return PromptResponse(
        generated_text=response.generated_text,
        provider=response.provider,
        model_id=response.model_id,
        request_id=response.request_id,
        usage_info=response.raw.get("usage", {}),
        raw_payload=response.raw_json()
    )

# Simple CLI example
# if __name__ == "__main__":
#     prompt = input("Prompt: ")
#     result = collect_platform_metadata(prompt)
#     print('\n--- METADATA ---')
#     print(json.dumps(result.raw_payload, indent=2))