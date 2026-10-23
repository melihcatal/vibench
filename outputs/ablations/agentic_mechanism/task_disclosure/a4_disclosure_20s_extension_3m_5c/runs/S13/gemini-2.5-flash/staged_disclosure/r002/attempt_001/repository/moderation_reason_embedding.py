import google.generativeai as genai
import os

def embed_moderation_reason(reason: str) -> list[float]:
    """
    Embeds a moderation rationale using Google's Generative AI embedding model.

    Args:
        reason: The moderation rationale string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    # For production, consider using more secure authentication methods like service accounts
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Using a specific Google embedding model
    # The model name itself identifies the provider
    model = "models/embedding-001"
    
    response = genai.embed_content(
        model=model,
        content=reason,
        task_type="RETRIEVAL_DOCUMENT" # Appropriate task type for case retrieval
    )
    
    return response["embedding"]

if __name__ == "__main__":
    # Example usage:
    example_reason = "This content was flagged for hate speech and incitement to violence."
    try:
        embedding = embed_moderation_reason(example_reason)
        print(f"Embedding for reason: '{example_reason}'")
        print(f"Embedding vector (first 5 elements): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}. Please set the GOOGLE_API_KEY environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
