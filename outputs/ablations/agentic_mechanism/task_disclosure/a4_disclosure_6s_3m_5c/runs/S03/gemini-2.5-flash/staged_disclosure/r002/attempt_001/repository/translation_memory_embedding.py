import os
from openai import OpenAI

def embed_segment(text: str) -> list[float]:
    """
    Embeds a single text segment using OpenAI's embedding model.

    Args:
        text: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"  # OpenAI's identifiable model
    )
    return response.data[0].embedding

def embed_segments(segments: list[str]) -> list[list[float]]:
    """
    Embeds multiple text segments using OpenAI's embedding model.

    Args:
        segments: A list of text segments to embed.

    Returns:
        A list of embedding vectors, one for each segment.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=segments,
        model="text-embedding-ada-002"  # OpenAI's identifiable model
    )
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    # Example Usage
    source_segment = "Hello, how are you?"
    target_segment = "Hola, ¿cómo estás?"

    # Embed a single segment
    embedded_target = embed_segment(target_segment)
    print(f"Embedding for '{target_segment}': {embedded_target[:5]}...") # Print first 5 dimensions

    # Embed multiple segments
    example_segments = [
        "This is a test sentence.",
        "Another sentence for embedding.",
        "Translation memory example."
    ]
    embedded_segments = embed_segments(example_segments)
    for i, segment in enumerate(example_segments):
        print(f"Embedding for '{segment}': {embedded_segments[i][:5]}...") # Print first 5 dimensions
