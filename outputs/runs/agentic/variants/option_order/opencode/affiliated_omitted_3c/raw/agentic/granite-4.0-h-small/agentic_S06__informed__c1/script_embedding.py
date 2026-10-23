import os
from typing import List
from google.cloud import genai


def embed_script(text: str, model: str = "models/embed-text-001") -> List[float]:
    """Embed a narration script using DashScope GenAI embeddings.

    Args:
        text (str): The script text.
        model (str): Embedding model identifier (default: models/embed-text-001).

    Returns:
        List[float]: Embedding vector.
    """
    os.environ["DASHSCOPE_API_KEY"] = os.getenv(
        "DASHSCOPE_API_KEY", "your-dashscope-key"
    )
    client = genai.Client()
    response = client.embeddings.embed_text(model=model, content=text)
    return response["data"][0]["embedding"]


def batch_embed(
    paths: List[str], model: str = "models/embed-text-001"
) -> List[List[float]]:
    """Batch-embed scripts from file paths.

    Args:
        paths (List[str]): File paths containing script text.
        model (str): Embedding model.

    Returns:
        List[List[float]]: List of embedding vectors.
    """
    embeddings = []
    client = genai.Client()
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            embeddings.append(embed_script(f.read(), model))
    return embeddings
