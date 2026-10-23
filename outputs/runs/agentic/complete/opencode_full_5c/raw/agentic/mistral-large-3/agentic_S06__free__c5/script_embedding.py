from google.cloud import aiplatform
from typing import List, Dict
import numpy as np


def embed_script(
    text: str, model_id: str = "textembedding-gecko@latest"
) -> List[float]:
    """
    Embeds narration scripts for voice-asset search using Google Cloud Vertex AI.
    """
    aiplatform.init()

    model = aiplatform.Model(model_name=model_id)
    endpoint = model.deployed_endpoints[0]

    response = endpoint.predict(instances=[{"content": text}])

    return response.predictions[0]


def batch_embed_scripts(
    texts: List[str], model_id: str = "textembedding-gecko@latest"
) -> List[List[float]]:
    """
    Embeds a batch of narration scripts for voice-asset search.
    """
    aiplatform.init()

    model = aiplatform.Model(model_name=model_id)
    endpoint = model.deployed_endpoints[0]

    response = endpoint.predict(instances=[{"content": text} for text in texts])

    return response.predictions


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Computes cosine similarity between two embeddings.
    """
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    return np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )
