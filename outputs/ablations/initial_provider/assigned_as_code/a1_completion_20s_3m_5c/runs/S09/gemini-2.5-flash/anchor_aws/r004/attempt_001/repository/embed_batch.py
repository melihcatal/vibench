import json

import numpy as np
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsInput, EmbeddingsOutput

def embed_batch(payloads, config=None):
    config = config or {}
    client_wrapper = EmbeddingsClient(region_name=config.get("region"))
    client = client_wrapper.get_client()
    
    embeddings = []
    for payload in payloads:
        bedrock_input = EmbeddingsInput(payload["text"])
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps(bedrock_input.to_json()),
            contentType="application/json",
            accept="application/json"
        )
        stream = response["body"]
        try:
            embedding_output = EmbeddingsOutput.from_json(json.loads(stream.read()))
            embeddings.append(embedding_output.embedding)
        finally:
            stream.close()
    return {"embeddings": embeddings}
