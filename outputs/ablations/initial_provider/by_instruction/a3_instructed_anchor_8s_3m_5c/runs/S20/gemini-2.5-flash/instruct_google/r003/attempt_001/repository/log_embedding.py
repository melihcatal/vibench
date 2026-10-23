import google.generativeai as genai
import os
from typing import List

def embed_log_message(log_message: str) -> List[float]:
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Use an embedding model, e.g., 'embedding-001'
    model = 'models/embedding-001'

    try:
        # The embed_content method returns an Embedding object
        response = genai.embed_content(
            model=model,
            content=log_message,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    # Example Usage:
    log_message_1 = "Database connection error: Timeout."
    log_message_2 = "Failed to connect to the primary database server."
    log_message_3 = "User login successful."

    embedding_1 = embed_log_message(log_message_1)
    embedding_2 = embed_log_message(log_message_2)
    embedding_3 = embed_log_message(log_message_3)

    print(f"\nEmbedding for \"{log_message_1}\": {embedding_1[:5]}...") # Print first 5 elements
    print(f"Embedding for \"{log_message_2}\": {embedding_2[:5]}...")
    print(f"Embedding for \"{log_message_3}\": {embedding_3[:5]}...")

    # You can then use these embeddings for similarity search, clustering, etc.
    # For instance, to calculate cosine similarity between embeddings:
    import numpy as np

    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    if embedding_1 and embedding_2 and embedding_3:
        similarity_1_2 = cosine_similarity(embedding_1, embedding_2)
        similarity_1_3 = cosine_similarity(embedding_1, embedding_3)

        print(f"\nCosine similarity between log 1 and log 2: {similarity_1_2:.4f}")
        print(f"Cosine similarity between log 1 and log 3: {similarity_1_3:.4f}")
