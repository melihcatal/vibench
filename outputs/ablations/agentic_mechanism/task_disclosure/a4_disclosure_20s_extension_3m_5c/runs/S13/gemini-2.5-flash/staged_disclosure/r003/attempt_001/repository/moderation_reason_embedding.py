import os
import openai

def embed_moderation_reason(reason: str) -> list[float]:
    """
    Embeds a moderation rationale using OpenAI's embedding model.

    Args:
        reason: The moderation rationale string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[reason],
        model="text-embedding-ada-002"  # OpenAI's identifiable model
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_reason = "This content violates our policy on hate speech due to derogatory remarks."
    embedding = embed_moderation_reason(example_reason)
    print(f"Embedding for the reason: {embedding[:5]}...") # Print first 5 dimensions for brevity
