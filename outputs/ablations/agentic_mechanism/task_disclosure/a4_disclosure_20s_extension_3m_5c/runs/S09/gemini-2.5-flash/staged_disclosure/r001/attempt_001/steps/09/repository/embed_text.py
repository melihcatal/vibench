import os
from openai import OpenAI

def get_text_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for a given text string using OpenAI.

    Args:
        text: The input text string.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_text = "This is an example sentence for embedding."
    embedding = get_text_embedding(example_text)
    print(f"Embedding for '{example_text}': {embedding[:5]}...") # Print first 5 dimensions
    print(f"Embedding dimension: {len(embedding)}")
