import os
import openai

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding vector for a given text string using OpenAI's API.

    Args:
        text: The input text string.
        model: The OpenAI model to use for embedding (default: "text-embedding-ada-002").

    Returns:
        A list of floats representing the embedding vector.
    """
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    text_to_embed = "This is an example text to embed."
    embedding = get_embedding(text_to_embed)

    if embedding:
        print(f"Embedding for '{text_to_embed}':")
        print(embedding[:5])  # Print first 5 dimensions of the embedding
        print(f"Embedding length: {len(embedding)}")
