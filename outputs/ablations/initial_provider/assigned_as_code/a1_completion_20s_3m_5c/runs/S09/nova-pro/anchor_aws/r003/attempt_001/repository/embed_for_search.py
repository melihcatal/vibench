import json

import boto3

from embeddings_client import get_bedrock_client
from embeddings_models import normalize_payload, normalize_response


def embed_for_search(query, documents, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    normalized_query = normalize_payload(query)
    normalized_documents = [normalize_payload(doc) for doc in documents]
    query_response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": normalized_query["text"]}),
        contentType="application/json",
        accept="application/json"
    )
    document_responses = []
    for doc in normalized_documents:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": doc["text"]}),
            contentType="application/json",
            accept="application/json"
        )
        document_responses.append(response)
    query_stream = query_response["body"]
    document_streams = [response["body"] for response in document_responses]
    try:
        query_embedding = normalize_response(json.loads(query_stream.read()))['embedding']
        document_embeddings = [normalize_response(json.loads(stream.read()))['embedding'] for stream in document_streams]
        return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
    finally:
        query_stream.close()
        for stream in document_streams:
            stream.close()