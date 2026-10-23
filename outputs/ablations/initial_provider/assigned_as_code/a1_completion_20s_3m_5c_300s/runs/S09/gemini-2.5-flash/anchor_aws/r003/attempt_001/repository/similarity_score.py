import numpy as np
from embeddings_client import BedrockEmbeddingsClient

def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def similarity_score(payload, config=None):
    config = config or {}
    client = BedrockEmbeddingsClient(
        region_name=config.get("region"),
        model_id="amazon.titan-embed-text-v2:0"
    )

    text1 = payload["text1"]
    text2 = payload["text2"]

    embedding1_response = client.invoke_model(text1)
    embedding1 = embedding1_response["embedding"]

    embedding2_response = client.invoke_model(text2)
    embedding2 = embedding2_response["embedding"]

    score = cosine_similarity(embedding1, embedding2)
    return {"similarity_score": score}
