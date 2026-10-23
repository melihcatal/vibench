import os
import cohere
from typing import List

def embed_log_message(text_to_embed: str) -> List[float]:
    """
    Embeds a log message for semantic retrieval using Cohere.

    Args:
        text_to_embed: The log message text.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[text_to_embed],
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

if __name__ == '__main__':
    log_message = "Database connection timed out for service payments-api"
    
    print(f"Embedding log message: '{log_message}'")
    
    embedding_vector = embed_log_message(log_message)
    
    if embedding_vector:
        print(f"Successfully generated embedding vector with dimension: {len(embedding_vector)}")
        print(f"First 5 dimensions: {embedding_vector[:5]}")
    else:
        print("Failed to generate embedding vector.")
