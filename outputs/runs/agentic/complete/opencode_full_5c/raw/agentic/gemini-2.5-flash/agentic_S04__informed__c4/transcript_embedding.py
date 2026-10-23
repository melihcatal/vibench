import os
from openai import OpenAI


def get_transcript_embedding(text: str) -> list[float]:
    """Embeds transcript segments for semantic retrieval using OpenAI Embeddings."""
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    # Use a specific OpenAI embedding model
    model_id = "text-embedding-ada-002"

    response = client.embeddings.create(input=[text], model=model_id)
    return response.data[0].embedding


if __name__ == "__main__":
    # Example usage
    # text_to_embed = "The quick brown fox jumps over the lazy dog."
    # embedding = get_transcript_embedding(text_to_embed)
    # print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
    # print(f"Embedding length: {len(embedding)}")
    pass
