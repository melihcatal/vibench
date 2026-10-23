import os
import openai

def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI's text-embedding-ada-002 model.

    Args:
        texts: A list of strings to generate embeddings for.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [embedding.embedding for embedding in response.data]

if __name__ == "__main__":
    # Example usage
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is a rapidly evolving field.",
        "Embeddings are numerical representations of text."
    ]
    try:
        embeddings = generate_embeddings_batch(sample_texts)
        for i, emb in enumerate(embeddings):
            print(f"Embedding for text {i+1}: {emb[:10]}...") # Print first 10 dimensions
        print(f"Generated {len(embeddings)} embeddings, each with dimension {len(embeddings[0])}.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
