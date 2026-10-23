import json

from embeddings_client import bedrock_client, model_id
from embeddings_models import normalize_embedding_response


def embed_for_search(payload, config=None):
    client = bedrock_client(config)
    query_response = client.invoke_model(modelId=model_id(config), body=json.dumps({"inputText": payload["query"]}), contentType="application/json", accept="application/json")
    query_stream = query_response["body"]
    try:
        query_embedding = normalize_embedding_response(json.loads(query_stream.read()))["embedding"]
    finally:
        query_stream.close()
    documents = payload.get("documents", [])
    doc_response = client.invoke_model(modelId=model_id(config), body=json.dumps({"inputTextList": documents}), contentType="application/json", accept="application/json")
    doc_stream = doc_response["body"]
    try:
        doc_embeddings = normalize_embedding_response(json.loads(doc_stream.read())).get("embeddings", [])
    finally:
        doc_stream.close()
    return {"query_embedding": query_embedding, "document_embeddings": doc_embeddings}
