import os
from huggingface_hub import InferenceClient


def stream_generation(model_id: str, prompt: str):
    """Streams output from a managed model platform while preserving provider response objects."""
    client = InferenceClient(model=model_id, token=os.environ.get("HF_TOKEN"))
    for token in client.text_generation(prompt, stream=True):
        yield {"token": token.token.text, "details": token.token.special}
