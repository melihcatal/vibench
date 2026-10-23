import os
from huggingface_hub import InferenceClient


def invoke_model(model_id: str, prompt: str) -> dict:
    """Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client."""
    client = InferenceClient(model=model_id, token=os.environ.get("HF_TOKEN"))
    response = client.text_generation(prompt)
    return {"generated_text": response}
