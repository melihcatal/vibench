import os

from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)


def stream_generation(model_id, inputs):
    response = client.text_generation(model=model_id, inputs=inputs, stream=True)
    for chunk in response:
        yield chunk
