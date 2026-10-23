import json
import numpy as np

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsInput, EmbeddingsOutput

def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def similarity_score(text1, text2, config=None):
    config = config or {}
    client_wrapper = EmbeddingsClient(region_name=config.get("region"))
    client = client_wrapper.get_client()

    # Embed text1
    bedrock_input1 = EmbeddingsInput(text1)
    response1 = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(bedrock_input1.to_json()),
        contentType="application/json",
        accept="application/json"
    )
    stream1 = response1["body"]
    try:
        embedding_output1 = EmbeddingsOutput.from_json(json.loads(stream1.read()))
        embedding1 = embedding_output1.embedding
    finally:
        stream1.close()

    # Embed text2
    bedrock_input2 = EmbeddingsInput(text2)
    response2 = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(bedrock_input2.to_json()),
        contentType="application/json",
        accept="application/json"
    )
    stream2 = response2["body"]
    try:
        embedding_output2 = EmbeddingsOutput.from_json(json.loads(stream2.read()))
        embedding2 = embedding_output2.embedding
    finally:
        stream2.close()

    score = cosine_similarity(np.array(embedding1), np.array(embedding2))
    return {"similarity_score": score.item()}
