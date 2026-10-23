import json

import boto3

from embeddings_client import get_bedrock_client, invoke_bedrock_text_embedding_model

def embed_for_search(payload, config=None):
    config = config or {}
    client = get_bedrock_client(region_name=config.get("region", "us-east-1"))

    query_embedding = invoke_bedrock_text_embedding_model(client, payload["query"], model_id="amazon.titan-embed-text-v2:0")
    
    document_embeddings = []
    for doc_text in payload["documents"]:
        document_embeddings.append(invoke_bedrock_text_embedding_model(client, doc_text, model_id="amazon.titan-embed-text-v2:0"))
        
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
