import os
import openai

def embed_translated_segment(segment: str) -> list[float]:
    """
    Embeds a translated segment using OpenAI's text-embedding-ada-002 model.

    Args:
        segment: The translated text segment to embed.

    Returns:
        A list of floats representing the embedding of the segment.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=[segment]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_segment = "This is an example translated segment."
    embedding = embed_translated_segment(example_segment)
    print(f"Embedding for segment: {example_segment[:30]}...")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 embedding values: {embedding[:5]}")
