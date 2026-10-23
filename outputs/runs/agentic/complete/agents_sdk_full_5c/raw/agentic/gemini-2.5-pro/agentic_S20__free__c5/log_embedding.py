import os
import cohere
from typing import List

def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using the Cohere API.
    These embeddings can be used for semantic search, clustering, or anomaly detection.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        return []

    try:
        # Initialize the Cohere client
        co = cohere.Client(api_key)

        print(f"Generating embeddings for {len(log_messages)} log messages...")

        # Call the embed API
        # Using a model optimized for retrieval tasks
        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        embeddings = response.embeddings
        print(f"Successfully generated {len(embeddings)} embeddings.")
        # print(f"Dimension of first embedding: {len(embeddings[0])}")

        return embeddings

    except Exception as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

if __name__ == '__main__':
    sample_logs = [
        "User failed to log in: invalid credentials for user 'admin'",
        "Authentication error: password does not meet complexity requirements.",
        "Database connection timed out after 30 seconds.",
        "Service is unavailable, backend connection refused.",
        "Successfully processed payment for order #98765.",
        "New user registration complete for user_id 'abc-123'.",
    ]
    
    log_embeddings = get_log_embeddings(sample_logs)
    
    if log_embeddings:
        # You would typically store these embeddings in a vector database
        # for later retrieval.
        print("\nExample of the first embedding (first 5 dimensions):")
        print(log_embeddings[0][:5])
