import os
import openai

def embed_moderation_reason(reason: str) -> list[float]:
    """
    Embeds a moderation rationale using OpenAI's embedding API.

    Args:
        reason: The moderation rationale string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # OpenAI API key should be set as an environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Using a specific OpenAI embedding model
    model_id = "text-embedding-ada-002"

    response = openai.embeddings.create(
        model=model_id,
        input=[reason]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage
    moderation_rationale = "This content contains hate speech and violates community guidelines."
    try:
        embedding = embed_moderation_reason(moderation_rationale)
        print(f"Embedding for the reason: {embedding[:5]}...") # Print first 5 dimensions
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
