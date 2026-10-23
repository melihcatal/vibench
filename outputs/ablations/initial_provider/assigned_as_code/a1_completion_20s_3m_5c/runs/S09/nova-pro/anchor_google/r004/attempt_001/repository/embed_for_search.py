import os

from amazon.bedrock import client


def embed_for_search(query, documents, config=None):
    config = config or {}
    with client.BedrockClient(api_key=config.get("api_key") or os.environ["AMAZON_BEDROCK_API_KEY"]) as client:
        query_embedding = client.models.embed_content(model="amazon-bedrock-embedding-001", contents=query)
        document_embeddings = client.models.embed_content(model="amazon-bedrock-embedding-001", contents=documents)
    return {"query_embedding": list(query_embedding.embeddings[0].values()), "document_embeddings": [list(embedding.values()) for embedding in document_embeddings.embeddings]}