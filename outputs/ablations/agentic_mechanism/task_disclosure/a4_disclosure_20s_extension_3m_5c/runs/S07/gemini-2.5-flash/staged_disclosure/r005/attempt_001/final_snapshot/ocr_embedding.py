import os
from openai import OpenAI

def get_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """
    Generates embeddings for a list of text documents using OpenAI's API.

    Args:
        texts: A list of strings, where each string is a document section.
        model: The OpenAI embedding model to use.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a document section.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=texts, model=model)
    return [data.embedding for data in response.data]

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY to be set in environment variables)
    document_sections = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is a rapidly evolving field.",
        "Semantic retrieval enhances search capabilities.",
    ]
    embeddings = get_embeddings(document_sections)
    for i, embedding in enumerate(embeddings):
        print(f"Embedding for section {i+1}: {embedding[:5]}...") # Print first 5 dimensions
        print(f"Length of embedding: {len(embedding)}")
