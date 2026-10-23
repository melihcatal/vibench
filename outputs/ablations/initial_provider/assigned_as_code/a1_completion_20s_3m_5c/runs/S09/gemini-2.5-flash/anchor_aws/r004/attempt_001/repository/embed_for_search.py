import json

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsInput, EmbeddingsOutput

def embed_for_search(query_text, document_texts, config=None):
    config = config or {}
    client_wrapper = EmbeddingsClient(region_name=config.get("region"))
    client = client_wrapper.get_client()

    # Embed query
    bedrock_input_query = EmbeddingsInput(query_text)
    response_query = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(bedrock_input_query.to_json()),
        contentType="application/json",
        accept="application/json"
    )
    stream_query = response_query["body"]
    try:
        embedding_output_query = EmbeddingsOutput.from_json(json.loads(stream_query.read()))
        query_embedding = embedding_output_query.embedding
    finally:
        stream_query.close()

    # Embed documents
    document_embeddings = []
    for doc_text in document_texts:
        bedrock_input_doc = EmbeddingsInput(doc_text)
        response_doc = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps(bedrock_input_doc.to_json()),
            contentType="application/json",
            accept="application/json"
        )
        stream_doc = response_doc["body"]
        try:
            embedding_output_doc = EmbeddingsOutput.from_json(json.loads(stream_doc.read()))
            document_embeddings.append(embedding_output_doc.embedding)
        finally:
            stream_doc.close()

    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
