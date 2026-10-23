import json
import numpy as np
from model_client import create_client
from model_models import normalize


def embed_output(text: str, model: str = "gpt-4o-mini") -> np.ndarray:
    """Embed model output for downstream tasks like clustering or retrieval.

    Args:
        text (str): The text to embed.
        model (str): Model family to use for embedding.

    Returns:
        np.ndarray: Normalized embedding vector (float32).
    """
    client = create_client(model)
    # Use the provider's embedding endpoint; here we approximate with a text completion
    # that returns a JSON vector. Adjust for your provider's real embeddings API.
    prompt = f"Return ONLY a JSON array of floating point numbers representing the embedding of the following text, no explanations:\n\n{text}"
    raw = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    vec_str = normalize(raw).choices[0].message.content.strip()
    vec = np.array(json.loads(vec_str), dtype=np.float32)
    # L2 normalize
    norm = np.linalg.norm(vec)
    if norm > 1e-6:
        vec = vec / norm
    return vec
