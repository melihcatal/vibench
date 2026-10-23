import openai
from embeddings_client import get_openai_client

def embed_batch(texts: list[str], model: str = "text-embedding-ada-002") -> list[list[float]]:
    """Generates embeddings for a batch of text strings using OpenAI.

    Args:
        texts: A list of text strings to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    client = get_openai_client()
    response = client.embeddings.create(input=texts, model=model)
    return [d.embedding for d in response.data]

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()
    # batch_embeddings = embed_batch(["Hello, world!", "How are you?"])
    # print(f"Number of embeddings: {len(batch_embeddings)}")
    # if batch_embeddings:
    #     print(f"First embedding length: {len(batch_embeddings[0])}")
    pass
