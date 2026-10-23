import os
from openai import OpenAI

def embed_transcript_segment(segment: str) -> list[float]:
    """
    Embeds a single transcript segment using OpenAI's text-embedding-ada-002 model.

    Args:
        segment: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.embeddings.create(
        input=segment,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    test_segment = "This is a test transcript segment for embedding."
    embedding = embed_transcript_segment(test_segment)
    print(f"Embedding for segment: '{test_segment}'")
    print(f"Embedding length: {len(embedding)}")
    # print(f"Embedding: {embedding}") # Uncomment to see the full embedding
