from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_for_search(query, documents, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    query_request = EmbeddingRequest(text=query).to_dict()
    document_requests = [EmbeddingRequest(text=doc).to_dict() for doc in documents]
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0",
                                   body=json.dumps({"query": query_request["text"],
                                                    "documents": [doc["text"] for doc in document_requests]},
                                                   default=str),
                                   contentType="application/json",
                                   accept="application/json")
    stream = response["body"]
    try:
        embeddings = json.loads(stream.read())["embeddings"]
        return [{"embedding": embedding} for embedding in embeddings]
    finally:
        stream.close()