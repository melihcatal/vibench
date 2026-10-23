import os

from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)


def collect_metadata(model_id, inputs):
    response = client.text_generation(model=model_id, inputs=inputs)
    metadata = {
        "usage": response.usage,
        "model_id": model_id,
    }
    return response.generated_text, metadata
