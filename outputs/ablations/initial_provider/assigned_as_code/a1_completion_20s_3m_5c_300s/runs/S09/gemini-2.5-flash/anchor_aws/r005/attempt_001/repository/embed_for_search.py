import json
import boto3
from embeddings_client import BedrockEmbeddingsClient
from embeddings_models import prepare_bedrock_payload, parse_bedrock_response

def embed_for_search(query, documents, config=None):
    config = config or {}
    bedrock_client_wrapper = BedrockEmbeddingsClient(region_name=config.get("region"))
    client = bedrock_client_wrapper.get_client()
    model_id = bedrock_client_wrapper.get_model_id()

    query_embedding = None
    if query:
        query_payload = prepare_bedrock_payload(query)
        query_response = client.invoke_model(modelId=model_id,
            body=query_payload, contentType="application/json", accept="application/json")
        query_embedding = parse_bedrock_response(query_response["body"])
    
    document_embeddings = []
    for doc in documents:
        doc_payload = prepare_bedrock_payload(doc)
        doc_response = client.invoke_model(modelId=model_id,
            body=doc_payload, contentType="application/json", accept="application/json")
        document_embeddings.append(parse_bedrock_response(doc_response["body"]))
        
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
