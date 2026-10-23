
import os
import openai

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding model.

    Args:
        text: The text string to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    caption_chunk = "This is a sample caption chunk from a meeting."
    embedding = get_embedding(caption_chunk)
    print(f"Embedding for '{caption_chunk[:30]}...': {embedding[:5]}...") # Print first 5 dimensions
    print(f"Embedding length: {len(embedding)}")
