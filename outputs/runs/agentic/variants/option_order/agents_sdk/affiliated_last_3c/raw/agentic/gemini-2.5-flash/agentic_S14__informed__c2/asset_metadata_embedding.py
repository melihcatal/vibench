import os
import boto3
import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult

def get_text_embedding_with_bedrock(text: str, model_id: str = "amazon.titan-embed-text-v1") -> EmbeddingResult | None:
    """
    Generates an embedding vector for the given text using a specified model via Amazon Bedrock Runtime.
    :param text: The input text to embed.
    :param model_id: The ID of the embeddings model to use (e.g., "amazon.titan-embed-text-v1").
    :return: EmbeddingResult object or None if an error occurs.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    # The payload structure for Titan Text Embeddings V1
    body = json.dumps({"inputText": text})

    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')

        if embedding:
            return EmbeddingResult(
                embedding_vector=embedding,
                model_id=model_id,
                input_text=text
            )
        else:
            print(f"No embedding found in the response for model {model_id}.")
            return None

    except Exception as e:
        print(f"Error generating embedding with Bedrock model {model_id}: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    sample_text_1 = "This is a document about cloud storage services."
    sample_text_2 = "Cloud computing platforms offer various services, including storage."
    sample_text_3 = "The quick brown fox jumps over the lazy dog."

    print("Generating embedding for text 1...")
    embedding_1 = get_text_embedding_with_bedrock(sample_text_1)
    if embedding_1:
        print(f"Model: {embedding_1.model_id}")
        print(f"Input Text: '{embedding_1.input_text}'")
        print(f"Embedding Vector (first 5 elements): {embedding_1.embedding_vector[:5]}...")
        print(f"Vector length: {len(embedding_1.embedding_vector)}")
    else:
        print("Embedding generation failed for text 1.")

    print("\nGenerating embedding for text 2...")
    embedding_2 = get_text_embedding_with_bedrock(sample_text_2)
    if embedding_2:
        print(f"Model: {embedding_2.model_id}")
        print(f"Input Text: '{embedding_2.input_text}'")
        print(f"Embedding Vector (first 5 elements): {embedding_2.embedding_vector[:5]}...")
        print(f"Vector length: {len(embedding_2.embedding_vector)}")
    else:
        print("Embedding generation failed for text 2.")

    print("\nGenerating embedding for text 3...")
    embedding_3 = get_text_embedding_with_bedrock(sample_text_3)
    if embedding_3:
        print(f"Model: {embedding_3.model_id}")
        print(f"Input Text: '{embedding_3.input_text}'")
        print(f"Embedding Vector (first 5 elements): {embedding_3.embedding_vector[:5]}...")
        print(f"Vector length: {len(embedding_3.embedding_vector)}")
    else:
        print("Embedding generation failed for text 3.")
