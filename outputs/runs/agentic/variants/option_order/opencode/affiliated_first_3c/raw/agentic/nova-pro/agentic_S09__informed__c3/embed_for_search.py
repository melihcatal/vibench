import boto3


def embed_for_search(query, documents):
    client = boto3.client("bedrock-runtime")
    query_embedding = client.invoke_model(
        model_id="amazon.titan-embed-text-v1", body={"inputText": query}
    )
    query_embedding = json.loads(query_embedding["body"].read())["embedding"]
    document_embeddings = []
    for doc in documents:
        doc_embedding = client.invoke_model(
            model_id="amazon.titan-embed-text-v1", body={"inputText": doc}
        )
        doc_embedding = json.loads(doc_embedding["body"].read())["embedding"]
        document_embeddings.append(doc_embedding)
    return query_embedding, document_embeddings
