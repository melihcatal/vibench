import boto3
import os
import json

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using AWS Bedrock.
    Returns the query embedding and a list of document embeddings.
    """
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    model_id = "amazon.titan-embed-text-v1"

    # Embed the query
    query_response = bedrock.invoke_model(
        body=f'{{"inputText": "{query}"}}',
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    query_embedding = json.loads(query_response.get("body").read())["embedding"]

    # Embed the documents
    document_embeddings = []
    for doc in documents:
        doc_response = bedrock.invoke_model(
            body=f'{{"inputText": "{doc}"}}',
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        document_embeddings.append(json.loads(doc_response.get("body").read())["embedding"])

    return query_embedding, document_embeddings
