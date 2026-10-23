from google.cloud import aiplatform
from typing import List
import numpy as np
import os


def embed_script(text: str) -> List[float]:
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_REGION"),
    )

    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")
    embeddings = model.get_embeddings([text])

    return embeddings[0].values
