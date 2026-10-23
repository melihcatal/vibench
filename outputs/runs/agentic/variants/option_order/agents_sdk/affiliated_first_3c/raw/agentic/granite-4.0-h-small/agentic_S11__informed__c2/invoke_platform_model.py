import os
from model_client import ManagedModelClient
from model_models import PromptRequest, PromptResponse

# ---------------------------------------------------------------------------
# Example: invoke a Hugging Face Inference API model
# ---------------------------------------------------------------------------

# Environment variables expected by Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL_ID")  # e.g. 'google/bigscience-bloom'

if not HF_TOKEN:
    raise RuntimeError("Set HF_TOKEN environment variable")
if not MODEL_ID:
    raise RuntimeError("Set HF_MODEL_ID environment variable")

def invoke_platform_model(prompt: str, max_tokens: int = 256) -> PromptResponse:
    """Invoke the selected Hugging Face model and return a PromptResponse object.

    Args:
        prompt (str): Input text for generation.
        max_tokens (int): Maximum number of tokens to generate.
    """
    client = ManagedModelClient(
        provider="huggingface",
        token=HF_TOKEN,
        model_id=MODEL_ID
    )
    # Create a PromptRequest compatible with Hugging Face API
    request = PromptRequest(
        inputs=prompt,
        parameters={
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.95
        }
    )
    response = client.invoke(request)
    # Wrap the raw API response in our local model response object
    return PromptResponse(
        generated_text=response.generated_text,
        provider=client.provider,
        request_id=response.request_id,
        raw=response.raw_json()
    )

# Simple CLI for demonstration
if __name__ == "__main__":
    user_input = input("Enter prompt: ")
    result = invoke_platform_model(user_input)
    print("\n--- RESPONSE FROM HUGGING FACE ---\n")
    print(result.generated_text)
