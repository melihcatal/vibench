import os
import numpy as np
from ibm_watsonx_ai import Client


class Embedder:
    def __init__(self):
        self.client = Client(
            instance_url=os.getenv("WATSONX_INSTANCE_URL"),
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        self.model_id = "granite-4.0-h-small"

    def embed(self, text):
        payload = {
            "model_id": self.model_id,
            "inputs": text,
            "parameters": {
                "use_embeddings": True,
                "max_new_tokens": 0,
                "temperature": 0,
            },
        }
        response = self.client.text_chat(completion=payload)
        # Assume response contains embeddings array
        embeddings = response.get("embeddings", [])
        return np.array(embeddings)


if __name__ == "__main__":
    embedder = Embedder()
    vec = embedder.embed("The quick brown fox")
    print("Embedding shape:", vec.shape)
