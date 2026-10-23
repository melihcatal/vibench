import google.generativeai as genai  # Provider-identifying signal
import os
from typing import List


def embed_text(
    text: str,
    model_name: str = "models/embedding-001",  # Model family
) -> List[float]:
    """Embeds object metadata and extracted text for search using Gemini Embeddings."""
    # Assumes GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    result = genai.embed_content(
        model=model_name, content=text, task_type="RETRIEVAL_DOCUMENT"
    )

    return result["embedding"]
