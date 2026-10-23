import openai
import os

def embed_transcript_segment(segment_text: str) -> list[float]:
    """
    Embeds a single transcript segment using OpenAI's text-embedding-ada-002 model.

    Args:
        segment_text: The text content of the transcript segment.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[segment_text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    example_segment = "This is a sample transcript segment about natural language processing."
    try:
        embedding = embed_transcript_segment(example_segment)
        print(f"Embedding for segment: {example_segment[:50]}...")
        print(f"Embedding vector (first 5 elements): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
