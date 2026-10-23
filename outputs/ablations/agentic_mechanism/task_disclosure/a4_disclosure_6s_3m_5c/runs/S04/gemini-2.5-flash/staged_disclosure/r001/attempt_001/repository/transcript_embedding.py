import openai
import os

def embed_segments(segments: list[str]) -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using OpenAI's embedding model.

    Args:
        segments: A list of transcript segments (strings).

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=segments
    )
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    # Example usage (replace with your actual segments)
    transcript_segments = [
        "This is the first segment of the transcript.",
        "The second segment talks about natural language processing.",
        "And here is the final part, discussing machine learning applications."
    ]

    try:
        embeddings = embed_segments(transcript_segments)
        for i, emb in enumerate(embeddings):
            print(f"Embedding for segment {i+1}: {emb[:5]}...") # Print first 5 dimensions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
