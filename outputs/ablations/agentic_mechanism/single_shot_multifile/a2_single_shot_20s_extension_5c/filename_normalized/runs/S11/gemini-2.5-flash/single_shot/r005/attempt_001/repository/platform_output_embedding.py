import os
import openai
from openai import OpenAI
from typing import List, Dict, Any

def embed_platform_output(text_content: str) -> Dict[str, Any]:
    """Embed platform outputs for evaluation or retrieval using OpenAI Embeddings."""
    # Ensure OPENAI_API_KEY environment variable is set.
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    try:
        response = client.embeddings.create(
            input=text_content,
            model="text-embedding-3-small" # Concrete model identifier
        )
        
        embedding = response.data[0].embedding
        usage = response.usage
        
        return {
            "embedding": embedding,
            "model": response.model,
            "token_usage": {
                "prompt_tokens": usage.prompt_tokens,
                "total_tokens": usage.total_tokens
            }
        }
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI embedding generation failed: {e}")
