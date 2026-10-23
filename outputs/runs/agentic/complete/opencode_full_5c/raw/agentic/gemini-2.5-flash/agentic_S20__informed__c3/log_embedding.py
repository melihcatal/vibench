import google.generativeai as genai
import os


def embed_log_message(log_message):
    """Embeds selected log messages for semantic retrieval using the Gemini Embeddings API.

    Args:
        log_message (str): The log message text to embed.

    Returns:
        list: A list of floats representing the embedding vector, or an error message.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        return {"error": "GOOGLE_API_KEY environment variable not set."}

    genai.configure(api_key=google_api_key)

    try:
        # The embedding model to use for text embedding
        # Refer to https://ai.google.dev/models/gemini for available models and their capabilities.
        model_name = "models/embedding-001"
        response = genai.embed_content(
            model=model_name,
            content=log_message,
            task_type="RETRIEVAL_DOCUMENT",  # or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION, CLUSTERING
        )
        return response["embedding"]
    except Exception as e:
        return {"error": f"Gemini Embeddings API failed: {e}"}


if __name__ == "__main__":
    # Example usage with different log messages
    messages_to_embed = [
        "User login successful for user 'alice'.",
        "Failed authentication attempt for user 'bob'.",
        "Database connection error: timeout.",
        "Service started successfully on port 8080.",
    ]

    print("\n--- Embedding Log Messages ---")
    for msg in messages_to_embed:
        embedding = embed_log_message(msg)
        print(f"Log Message: '{msg}'")
        if isinstance(embedding, list):
            print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
            print(f"Embedding dimension: {len(embedding)}")
        else:
            print(f"Error: {embedding}")
        print("---")
