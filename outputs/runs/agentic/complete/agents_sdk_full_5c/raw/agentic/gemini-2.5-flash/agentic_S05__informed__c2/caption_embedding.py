import os
from typing import List
import openai

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding API.
    Requires OPENAI_API_KEY environment variable to be set.

    Args:
        text: The text string to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = text.replace("\n", " ") # Replace newlines with spaces for better embedding results
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def embed_caption_chunk(caption_chunk: str) -> List[float]:
    """
    Embeds a single caption chunk for semantic search.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable for OpenAI Embeddings.")
        return []

    if not caption_chunk.strip():
        print("Warning: Attempted to embed an empty caption chunk.")
        return []

    try:
        embedding = get_embedding(caption_chunk)
        return embedding
    except Exception as e:
        print(f"Error generating caption embedding: {e}")
        return []

if __name__ == "__main__":
    # Set your OPENAI_API_KEY environment variable
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

    # example_caption_1 = "The team discussed the Q3 financial performance."
    # embedding_1 = embed_caption_chunk(example_caption_1)
    # print(f"Embedding for \"{example_caption_1}\" (first 5 elements): {embedding_1[:5]}...")
    # print(f"Embedding length: {len(embedding_1)}")

    # example_caption_2 = "Sales figures showed a significant increase."
    # embedding_2 = embed_caption_chunk(example_caption_2)
    # print(f"Embedding for \"{example_caption_2}\" (first 5 elements): {embedding_2[:5]}...")

    # example_caption_empty = "   "
    # embedding_empty = embed_caption_chunk(example_caption_empty)
    # print(f"Embedding for empty caption: {embedding_empty}")

    # You can then use these embeddings for semantic similarity search, e.g.,
    # from scipy.spatial.distance import cosine
    # if embedding_1 and embedding_2:
    #     similarity = 1 - cosine(embedding_1, embedding_2)
    #     print(f"Cosine similarity between caption 1 and 2: {similarity}")
    pass
