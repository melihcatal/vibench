import os
from openai import OpenAI

def get_caption_embedding(caption_chunk: str) -> list[float]:
    """
    Embeds a single caption chunk using OpenAI's embedding service.

    Args:
        caption_chunk: The text chunk to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Using a concrete OpenAI embedding model
    model_name = "text-embedding-ada-002" 

    try:
        response = client.embeddings.create(
            input=caption_chunk,
            model=model_name
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error embedding caption chunk: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Ensure OPENAI_API_KEY environment variable is set
    
    test_caption = "This is a test caption chunk about meeting discussions."
    embedding = get_caption_embedding(test_caption)

    if embedding:
        print(f"Embedding for '{test_caption}': {embedding[:5]}...") # Print first 5 dimensions
        print(f"Embedding length: {len(embedding)}")
    else:
        print("Failed to get embedding.")
