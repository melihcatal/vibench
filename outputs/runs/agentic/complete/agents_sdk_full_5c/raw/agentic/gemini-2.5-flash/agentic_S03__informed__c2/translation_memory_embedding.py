import os
from openai import OpenAI
from typing import List

def get_embedding_for_text(text: str) -> List[float]:
    """
    Embeds a single text segment using OpenAI Embeddings for translation-memory search.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-ada-002" # OpenAI's embedding model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

def get_embeddings_for_texts(texts: List[str]) -> List[List[float]]:
    """
    Embeds multiple text segments using OpenAI Embeddings.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-ada-002"
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return []

if __name__ == '__main__':
    # Example usage (ensure OPENAI_API_KEY is set in environment variables)
    text_segment = "This is a translated segment."
    embedding = get_embedding_for_text(text_segment)
    print(f"Embedding for \"{text_segment}\": {embedding[:5]}...") # Print first 5 elements

    text_segments = [
        "Hello world",
        "Bonjour le monde"
    ]
    embeddings = get_embeddings_for_texts(text_segments)
    print(f"\nEmbeddings for multiple texts (first 5 elements of first embedding): {embeddings[0][:5]}...")
