import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform output using OpenAI's embedding model.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding of the input text.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  # Concrete model identifier
            input=[text]
        )
        # Assuming the response structure contains data[0].embedding
        return response.data[0].embedding
    except Exception as e:
        print(f"Error embedding text: {e}")
        raise
