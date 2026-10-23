from typing import List, Dict, Any
import numpy as np
from model_client import LLMClient
from model_models import LLMRequest


async def embed_output(text: str) -> List[float]:
    """Embed model outputs for clustering or retrieval using Mistral's hosted LLM."""
    client = LLMClient()
    prompt = (
        f"Generate a dense vector embedding for the following text. "
        f"Return the embedding as a JSON array of floats.\n\n"
        f"Text: {text}\n\n"
        f"Embedding:"
    )
    request = LLMRequest(prompt=prompt, max_tokens=50)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    await client.close()

    content = response["choices"][0]["message"]["content"]
    import json

    embedding = json.loads(content)
    return np.array(embedding, dtype=np.float32).tolist()
