import os
import google.generativeai as genai
from observability_client import configure_gemini_client
from observability_models import EmbeddingRequest
from typing import List

def embed_log_messages(embedding_request: EmbeddingRequest) -> List[float]:
    """
    Embeds selected log messages for semantic retrieval using the Google Gemini Embeddings API.
    """
    try:
        configure_gemini_client()
    except ValueError as e:
        print(f"Error configuring Gemini client: {e}")
        return []

    # The embedding model
    embedding_model = "models/embedding-001"

    try:
        response = genai.embed_content(
            model=embedding_model,
            content=embedding_request.text_content,
            task_type="SEMANTIC_SIMILARITY" # Other types include "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", "CLASSIFICATION"
        )
        # The embedding is in response['embedding']
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    # Example log messages
    log_message_1 = "User login successful from IP 192.168.1.1."
    log_message_2 = "Failed login attempt detected for user 'admin' from 192.168.1.2."
    log_message_3 = "Database connection error: timeout occurred."
    log_message_4 = "User 'guest' logged in successfully."
    log_message_5 = "Failed to connect to primary database."

    print("--- Embedding log_message_1 (successful login) ---")
    embed_req_1 = EmbeddingRequest(text_content=log_message_1)
    embedding_1 = embed_log_messages(embed_req_1)
    print(f"Embedding for '{log_message_1}': {embedding_1[:5]}...") # Print first 5 elements

    print("\n--- Embedding log_message_2 (failed login) ---")
    embed_req_2 = EmbeddingRequest(text_content=log_message_2)
    embedding_2 = embed_log_messages(embed_req_2)
    print(f"Embedding for '{log_message_2}': {embedding_2[:5]}...")

    print("\n--- Embedding log_message_3 (database error) ---")
    embed_req_3 = EmbeddingRequest(text_content=log_message_3)
    embedding_3 = embed_log_messages(embed_req_3)
    print(f"Embedding for '{log_message_3}': {embedding_3[:5]}...")

    print("\n--- Embedding log_message_4 (successful login again) ---")
    embed_req_4 = EmbeddingRequest(text_content=log_message_4)
    embedding_4 = embed_log_messages(embed_req_4)
    print(f"Embedding for '{log_message_4}': {embedding_4[:5]}...")
    
    print("\n--- Embedding log_message_5 (database error again) ---")
    embed_req_5 = EmbeddingRequest(text_content=log_message_5)
    embedding_5 = embed_log_messages(embed_req_5)
    print(f"Embedding for '{log_message_5}': {embedding_5[:5]}...")

    # You could then use these embeddings to calculate similarity,
    # e.g., using numpy.dot(embedding_1, embedding_4) to see similarity between successful logins.
    # (Requires numpy, not included in this snippet)
