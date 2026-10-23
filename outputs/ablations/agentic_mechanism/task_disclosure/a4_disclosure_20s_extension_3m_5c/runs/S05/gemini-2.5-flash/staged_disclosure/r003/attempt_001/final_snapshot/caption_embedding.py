import openai
import os

def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds a list of caption chunks using OpenAI's text-embedding-ada-002 model.

    Args:
        caption_chunks: A list of strings, where each string is a caption chunk.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Embedding.create(
        input=caption_chunks,
        model="text-embedding-ada-002"
    )
    embeddings = [data.embedding for data in response.data]
    return embeddings

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY to be set in environment)
    chunks = [
        "This is the first caption chunk about a meeting.",
        "The second chunk discusses the key decisions made.",
        "Finally, we summarize the action items for the team."
    ]
    try:
        embedded_chunks = embed_caption_chunks(chunks)
        print(f"Generated {len(embedded_chunks)} embeddings, each with dimension {len(embedded_chunks[0])}.")
        # print(embedded_chunks) # Uncomment to see the actual embeddings
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
