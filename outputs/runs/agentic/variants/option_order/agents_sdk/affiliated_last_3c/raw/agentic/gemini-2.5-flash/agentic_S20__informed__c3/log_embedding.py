import os
import google.generativeai as genai

# Ensure GOOGLE_API_KEY is set as an environment variable
# export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

def embed_log_message(text: str) -> list[float]:
    """
    Generates an embedding for a given log message using the Google Gemini Embeddings API.

    Args:
        text: The log message text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    try:
        # Use the 'embedding-001' model for embeddings.
        # See https://ai.google.dev/models/gemini for available models.
        response = genai.embed_content(
            model='models/embedding-001',
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # or "SEMANTIC_SIMILARITY", "AQA_QUESTION", etc.
        )
        # The embedding is in response['embedding']
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_API_KEY environment variable is set.

    log_message_1 = "User login failed due to incorrect password for user 'alice'."
    log_message_2 = "Failed to authenticate user 'bob'. Invalid credentials provided."
    log_message_3 = "Database connection error: Timeout occurred while connecting to primary replica."
    log_message_4 = "Application started successfully on port 8080."

    print(f"Embedding for message 1: \"{log_message_1}\"")
    embedding_1 = embed_log_message(log_message_1)
    print(f"Embedding (first 5 elements): {embedding_1[:5]}...")
    print(f"Embedding dimension: {len(embedding_1)}")
    print("-" * 30)

    print(f"Embedding for message 2: \"{log_message_2}\"")
    embedding_2 = embed_log_message(log_message_2)
    print(f"Embedding (first 5 elements): {embedding_2[:5]}...")
    print(f"Embedding dimension: {len(embedding_2)}")
    print("-" * 30)

    print(f"Embedding for message 3: \"{log_message_3}\"")
    embedding_3 = embed_log_message(log_message_3)
    print(f"Embedding (first 5 elements): {embedding_3[:5]}...")
    print(f"Embedding dimension: {len(embedding_3)}")
    print("-" * 30)

    print(f"Embedding for message 4: \"{log_message_4}\"")
    embedding_4 = embed_log_message(log_message_4)
    print(f"Embedding (first 5 elements): {embedding_4[:5]}...")
    print(f"Embedding dimension: {len(embedding_4)}")
    print("-" * 30)

    # In a real application, you would store these embeddings in a vector database
    # and use them for semantic search, anomaly detection, etc.
