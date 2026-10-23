import os
from huggingface_hub import InferenceClient


def collect_metadata(model_id: str, prompt: str) -> dict:
    """Returns model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    client = InferenceClient(model=model_id, token=os.environ.get("HF_TOKEN"))
    response = client.text_generation(prompt, details=True)

    # Hugging Face InferenceClient provides some details in the response
    metadata = {
        "generated_text": response.generated_text,
        "details": response.details.to_dict() if response.details else {},
        "model_id": model_id,
        # Other metadata could be inferred or added if available from the client or response
    }
    return metadata
