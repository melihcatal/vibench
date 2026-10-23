import os
import openai
# Ensure OPENAI_API_KEY is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not configured")

SDK_PROVIDER = "OpenAI"

def embed_script(text: str) -> list[float]:
    """Generate an embedding vector for a narration script using OpenAI embeddings.
    Returns a list of floats representing the vector.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    vector = response["data"][0]["embedding"]
    return vector

# Example integration with a vector database (e.g., Pinecone, Weaviate) would go here.
