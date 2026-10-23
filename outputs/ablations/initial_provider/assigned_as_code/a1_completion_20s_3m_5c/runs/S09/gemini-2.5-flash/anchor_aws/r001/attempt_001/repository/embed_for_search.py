import json

from embeddings_client import get_bedrock_client
from embeddings_models import create_titan_text_embedding_payload, parse_titan_text_embedding_response


def embed_for_search(query_text, document_texts, config=None):
    config = config or {}
    client = get_bedrock_client(config.get("region", "us-east-1"))

    # Embed the query
    query_response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=create_titan_text_embedding_payload(query_text),
        contentType="application/json",
        accept="application/json",
    )
    query_stream = query_response["body"]
    try:
        query_embedding = parse_titan_text_embedding_response(query_stream)
    finally:
        query_stream.close()

    # Embed the documents
    document_embeddings = []
    for doc_text in document_texts:
        doc_response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=create_titan_text_embedding_payload(doc_text),
            contentType="application/json",
            accept="application/json",
        )
        doc_stream = doc_response["body"]
        try:
            document_embeddings.append(parse_titan_text_embedding_response(doc_stream))
        finally:
            doc_stream.close()

    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
