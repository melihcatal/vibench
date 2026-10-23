import os
from typing import List
from observability_client import get_gemini_model
from observability_models import EmbeddingRequest

def embed_log_message(request: EmbeddingRequest) -> List[float]:
    """
    Embeds selected log messages for semantic retrieval using Gemini Embeddings.
    """
    model = get_gemini_model(model_name="embedding-001") # Using the specific embedding model

    if not request.text_content:
        return []

    print(f"Generating embedding for log message: '{request.text_content[:50]}...'")
    try:
        # The `embed_content` method is for embedding, and it expects a list of texts or a single text
        # using the models.embedText method if you want to use the specific API call
        # For simplicity with the GenerativeModel, we can pass text directly.
        response = model.embed_content(
            model="embedding-001",
            content=request.text_content
        )
        embedding = response['embedding']
        print(f"Embedding generated (length: {len(embedding)}).")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_API_KEY environment variable
    log_message1 = "User login failed due to incorrect password."
    log_message2 = "Authentication attempt failed: invalid credentials provided."
    log_message3 = "Database connection timed out during a read operation."

    embedding_request1 = EmbeddingRequest(text_content=log_message1)
    embedding_request2 = EmbeddingRequest(text_content=log_message2)
    embedding_request3 = EmbeddingRequest(text_content=log_message3)

    print("\n--- Embedding log message 1 ---")
    embedding1 = embed_log_message(embedding_request1)
    # print(embedding1) # Uncomment to see the full embedding

    print("\n--- Embedding log message 2 ---")
    embedding2 = embed_log_message(embedding_request2)

    print("\n--- Embedding log message 3 ---")
    embedding3 = embed_log_message(embedding_request3)

    # You can now use these embeddings for similarity searches, clustering, etc.
    # For example, a simple dot product for similarity between 1 and 2
    if embedding1 and embedding2:
        from numpy import dot
        similarity = dot(embedding1, embedding2)
        print(f"\nSimilarity between message 1 and 2: {similarity}")
