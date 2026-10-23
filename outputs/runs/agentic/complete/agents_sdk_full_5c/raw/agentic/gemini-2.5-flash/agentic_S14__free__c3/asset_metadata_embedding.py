import os
import boto3
import json
from typing import List
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult

def create_text_embedding(text_to_embed: str) -> EmbeddingResult or None:
    """
    Generates an embedding for the given text using Amazon Titan Embeddings via AWS Bedrock.

    Args:
        text_to_embed (str): The text content to embed.

    Returns:
        EmbeddingResult or None: An EmbeddingResult object containing the vector and model ID, or None if an error occurs.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1" # Amazon Titan Text Embedding v1

    # The request body for Titan Embeddings
    body = json.dumps({"inputText": text_to_embed})

    try:
        print(f"Invoking Bedrock model '{model_id}' for text embedding...")
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get('body').read())
        embedding_vector = response_body.get('embedding')

        if embedding_vector:
            print("Embedding generation successful.")
            return EmbeddingResult(
                embedding=embedding_vector,
                model_id=model_id,
                input_text=text_to_embed
            )
        else:
            print("No embedding found in the model response.")
            return None

    except Exception as e:
        print(f"Error creating text embedding with Bedrock: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    # This example assumes you have text (e.g., object metadata, extracted text) to embed.
    # Ensure AWS credentials are configured and Bedrock access is granted to Titan Embeddings.

    _sample_text_1 = "This is a document about machine learning models and their applications."
    _sample_text_2 = "Machine learning is a field of artificial intelligence that uses statistical techniques."
    _sample_text_3 = "The quick brown fox jumps over the lazy dog."

    print(f"\nEmbedding for: \"{_sample_text_1}\" ")
    embedding_result_1 = create_text_embedding(_sample_text_1)
    if embedding_result_1:
        print(f"  Embedding vector length: {len(embedding_result_1.embedding)}")
        print(f"  First 5 dimensions: {embedding_result_1.embedding[:5]}")
    else:
        print("  Failed to create embedding.")

    print(f"\nEmbedding for: \"{_sample_text_2}\" ")
    embedding_result_2 = create_text_embedding(_sample_text_2)
    if embedding_result_2:
        print(f"  Embedding vector length: {len(embedding_result_2.embedding)}")
        print(f"  First 5 dimensions: {embedding_result_2.embedding[:5]}")
    else:
        print("  Failed to create embedding.")

    print(f"\nEmbedding for: \"{_sample_text_3}\" ")
    embedding_result_3 = create_text_embedding(_sample_text_3)
    if embedding_result_3:
        print(f"  Embedding vector length: {len(embedding_result_3.embedding)}")
        print(f"  First 5 dimensions: {embedding_result_3.embedding[:5]}")
    else:
        print("  Failed to create embedding.")
