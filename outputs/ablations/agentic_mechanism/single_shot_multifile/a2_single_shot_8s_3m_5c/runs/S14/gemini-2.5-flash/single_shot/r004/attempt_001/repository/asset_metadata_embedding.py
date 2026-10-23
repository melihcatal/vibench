import os
from openai import OpenAI
from typing import List, Dict, Any
import hashlib

def embed_asset_data(
    text_to_embed: str,
    model: str = "text-embedding-3-small"
) -> dict:
    if not os.getenv('OPENAI_API_KEY'):
        return {"status": "error", "message": "OPENAI_API_KEY environment variable not set."}

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if not text_to_embed.strip():
        return {"status": "error", "message": "Input text for embedding cannot be empty."}

    try:
        response = client.embeddings.create(
            model=model,
            input=text_to_embed
        )
        embedding = response.data[0].embedding
        original_text_hash = hashlib.sha256(text_to_embed.encode('utf-8')).hexdigest()
        return {"status": "success", "embedding": embedding, "model_used": model, "original_text_hash": original_text_hash}
    except Exception as e:
        return {"status": "error", "message": str(e)}
