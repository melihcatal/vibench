from google.cloud import aiplatform
import os
import numpy as np


class ScriptEmbedder:
    def __init__(self):
        aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        self.model = aiplatform.TextEmbeddingModel.from_pretrained(
            "textembedding-gecko@latest"
        )

    def embed_script(self, text: str) -> list:
        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values
