import openai
import os

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a given text string using OpenAI's API."""
    # Ensure the OpenAI API key is set as an environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Use a specific embedding model
    model = "text-embedding-ada-002" 

    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

if __name__ == "__main__":
    sample_text = "Hello, world! This is a test sentence for embedding."
    try:
        embedding = embed_text(sample_text)
        print(f"Embedding for '{sample_text}' (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
