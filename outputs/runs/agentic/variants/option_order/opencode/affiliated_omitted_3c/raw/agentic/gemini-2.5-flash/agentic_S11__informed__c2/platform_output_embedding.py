from model_client import get_bedrock_client
from model_models import EmbeddingRequest, EmbeddingResponse
import os
import json


def embed_platform_output(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embed platform outputs for evaluation or retrieval using Amazon Titan Embeddings via Bedrock Runtime.
    """
    client = get_bedrock_client()
    model_id = "amazon.titan-embed-text-v1"  # Amazon Titan Embeddings model ID
    content_type = "application/json"
    accept = "application/json"

    body = request.to_bedrock_titan_payload()

    response = client.invoke_model(
        body=body, modelId=model_id, contentType=content_type, accept=accept
    )
    return EmbeddingResponse(response)


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    embedding_request = EmbeddingRequest(
        text="This is a sample sentence for embedding."
    )
    embedding_response = embed_platform_output(embedding_request)
    print(f"Text: {embedding_request.text}")
    print(f"Embedding (first 5 values): {embedding_response.embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding_response.embedding)}")

    embedding_request_2 = EmbeddingRequest(text="Another sentence to embed.")
    embedding_response_2 = embed_platform_output(embedding_request_2)
    print(f"Text: {embedding_request_2.text}")
    print(f"Embedding (first 5 values): {embedding_response_2.embedding[:5]}...")
