import openai
import os

def embed_log_message(log_message: str) -> list[float]:
    """
    Embeds a single log message using OpenAI's embedding API.

    Args:
        log_message: The log message to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Using a specific OpenAI embedding model
    model_id = "text-embedding-ada-002"

    response = openai.embeddings.create(
        input=[log_message],
        model=model_id
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage
    test_log_message = "ERROR: Failed to connect to database."
    try:
        embedding = embed_log_message(test_log_message)
        print(f"Embedding for '{test_log_message}': {embedding[:5]}...") # Print first 5 elements
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
