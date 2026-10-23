import openai
import os

def embed_segments(segments: list[str]) -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using OpenAI's embedding API.

    Args:
        segments: A list of strings, where each string is a transcript segment.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a segment.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=segments,
        model="text-embedding-ada-002"
    )
    return [embedding.embedding for embedding in response.data]

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY to be set in environment)
    example_segments = [
        "This is the first segment of the transcript.",
        "The second segment discusses important details.",
        "Finally, we conclude with a summary of the meeting."
    ]
    try:
        embeddings = embed_segments(example_segments)
        for i, emb in enumerate(embeddings):
            print(f"Embedding for segment {i+1} (first 5 values): {emb[:5]}...")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
