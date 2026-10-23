import json

from embeddings_client import get_bedrock_client
from embeddings_models import create_titan_text_embedding_payload, parse_titan_text_embedding_response


def embed_batch(texts, config=None):
    config = config or {}
    client = get_bedrock_client(config.get("region", "us-east-1"))
    embeddings = []
    for text in texts:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=create_titan_text_embedding_payload(text),
            contentType="application/json",
            accept="application/json",
        )
        stream = response["body"]
        try:
            embeddings.append(parse_titan_text_embedding_response(stream))
        finally:
            stream.close()
    return {"embeddings": embeddings}
