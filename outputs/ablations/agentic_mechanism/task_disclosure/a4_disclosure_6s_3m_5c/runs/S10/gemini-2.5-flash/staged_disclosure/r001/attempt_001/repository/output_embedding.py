import openai
import os

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using OpenAI's embedding model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_text = "This is an example sentence to be embedded."
    embedding = embed_text(example_text)
    print(f"Embedding for '{example_text}': {embedding[:5]}...") # Print first 5 dimensions
    print(f"Embedding length: {len(embedding)}")
