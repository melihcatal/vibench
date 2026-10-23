import os
from huggingface_hub import InferenceClient


class ModelClient:
    def __init__(self, model_id: str):
        self.client = InferenceClient(model=model_id, token=os.environ.get("HF_TOKEN"))

    def generate_text(self, prompt: str, stream: bool = False, details: bool = False):
        if stream:
            return self.client.text_generation(prompt, stream=True)
        else:
            return self.client.text_generation(prompt, details=details)
