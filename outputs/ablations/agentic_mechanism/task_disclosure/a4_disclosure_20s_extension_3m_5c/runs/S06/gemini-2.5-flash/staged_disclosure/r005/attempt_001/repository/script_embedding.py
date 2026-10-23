
import os
from openai import OpenAI

def embed_script(text: str) -> list[float]:
    """
    Embeds a given narration script using OpenAI's embedding service.

    Args:
        text: The narration script to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Initialize the OpenAI client.
    # Ensure OPENAI_API_KEY environment variable is set.
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Create an embedding for the given text
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"  # Concrete OpenAI model identifier
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    script_example = "This is an example narration script for voice asset search."
    embedding = embed_script(script_example)
    print(f"Embedding for the script: {embedding[:5]}...") # Print first 5 dimensions
    print(f"Embedding dimension: {len(embedding)}")
