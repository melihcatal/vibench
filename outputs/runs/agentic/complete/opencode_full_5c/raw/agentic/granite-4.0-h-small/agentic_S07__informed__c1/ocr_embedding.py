import openai
import os

# Direct OpenAI Embeddings API integration
# Provider identifiable via OPENAI_API_KEY env var and openai SDK import


def embed_sections(
    texts: List[str], model: str = "text-embedding-ada-002"
) -> List[Dict[str, Any]]:
    """Generate embeddings for a list of document sections using OpenAI API."""
    # Ensure the key is present in the environment
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    # Call the embeddings endpoint (supports batch up to 8000 tokens per request)
    response = openai.Embedding.create(model=model, input=texts)
    # Return a list of embedding vectors with their corresponding text (placeholder shape)
    return [
        {"text": item["input"], "embedding": item["embedding"], "model": model}
        for item in response["data"]
    ]
