import openai
from embeddings_client import get_openai_client

def embed_text(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """Generates an embedding vector for a single text string using OpenAI.

    Args:
        text: The text string to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = get_openai_client()
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()
    # embedding = embed_text("Hello, world!")
    # print(f"Embedding length: {len(embedding)}")
    # print(f"First 5 dimensions: {embedding[:5]}")
    pass
