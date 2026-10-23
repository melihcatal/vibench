import os
from openai import OpenAI

def embed_moderation_rationales(rationales: list[str]) -> list[list[float]]:
    """Embed moderation rationales for case retrieval using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    embeddings = []
    for rationale in rationales:
        try:
            # Using a common embedding model, e.g., text-embedding-ada-002 or text-embedding-3-small
            response = client.embeddings.create(
                input=[rationale],
                model="text-embedding-ada-002"
            )
            embeddings.append(response.data[0].embedding)
        except Exception as e:
            print(f"Error embedding rationale '{rationale}' with OpenAI: {e}")
            embeddings.append([]) # Append empty list or handle error as appropriate
    return embeddings
