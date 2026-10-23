import os

from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)


def select_model(model_id):
    model_info = client.model_info(model_id)
    return model_info
