import os
import json
import requests

# OpenAI embeddings endpoint (example provider)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"


def embed_script(text: str) -> Dict[str, Any]:
    """Generate a text embedding for a narration script using OpenAI Embeddings API.

    Args:
        text: The script to embed.

    Returns:
        JSON response containing the embedding vector and metadata.
    """
    payload = {"model": "text-embedding-ada-002", "input": text}
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(EMBEDDING_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


# Example usage (remove in production)
if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    print(embed_script(sample))
