import os
import openai

def embed_text(text: str) -> list[float]:
    """
    Embeds a given text using OpenAI's text-embedding-ada-002 model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_text = "This is an example document section."
    embedding = embed_text(example_text)
    print(f"Embedding for the text: {embedding[:5]}...") # Print first 5 elements
    print(f"Embedding length: {len(embedding)}")
