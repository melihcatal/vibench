import os
import openai

def embed_moderation_reason(reason: str) -> list[float]:
    """
    Embeds a moderation rationale using OpenAI's embedding model.

    Args:
        reason: The moderation rationale text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY="your_api_key_here"
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = os.environ["OPENAI_API_KEY"]

    try:
        response = openai.embeddings.create(
            input=reason,
            model="text-embedding-ada-002"  # Concrete OpenAI model identifier
        )
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    rationale = "This content promotes hate speech against a protected group."
    try:
        embedding = embed_moderation_reason(rationale)
        print(f"Embedding generated (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
