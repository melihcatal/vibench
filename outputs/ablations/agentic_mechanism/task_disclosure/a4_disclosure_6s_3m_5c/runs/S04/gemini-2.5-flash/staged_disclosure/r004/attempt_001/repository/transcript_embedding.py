import openai
import os

def embed_transcript_segment(segment: str) -> list[float]:
    """
    Embeds a single transcript segment using OpenAI's embedding API.

    Args:
        segment: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Concrete OpenAI model identifier
        input=segment
    )
    return response.data[0].embedding

if __name__ == "__main__":
    test_segment = "This is a test transcript segment about natural language processing."
    try:
        embedding = embed_transcript_segment(test_segment)
        print(f"Embedding generated (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the OPENAI_API_KEY environment variable.")
