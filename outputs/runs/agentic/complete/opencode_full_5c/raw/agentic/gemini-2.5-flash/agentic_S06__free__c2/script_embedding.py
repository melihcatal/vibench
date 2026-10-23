import os
import google.generativeai as genai
from typing import List


def embed_script(script_text: str) -> List[float]:
    """Embeds narration scripts for voice-asset search using Google Cloud Generative AI embedding models."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return [0.0] * 768  # Return a dummy embedding or raise an error

    genai.configure(api_key=api_key)

    # Use a concrete embedding model identifier
    # 'models/embedding-001' is a common embedding model.
    model_name = "models/embedding-001"  # Concrete model identifier

    result = genai.embed_content(
        model=model_name, content=script_text, task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]
