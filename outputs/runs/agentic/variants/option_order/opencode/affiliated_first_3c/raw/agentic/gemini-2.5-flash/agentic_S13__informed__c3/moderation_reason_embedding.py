import os
import google.generativeai as genai
from typing import List


def embed_moderation_reason(reason_texts: List[str]) -> List[List[float]]:
    google_api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")
    if not google_api_key or "YOUR_GOOGLE_API_KEY" in google_api_key:
        raise ValueError(
            "Google API Key must be set in environment variable GOOGLE_API_KEY"
        )

    genai.configure(api_key=google_api_key)

    # The embedding model to use. For Gemini, 'embedding-001' is a common choice.
    model_name = "embedding-001"

    embeddings = []
    for text in reason_texts:
        response = genai.embed_content(model=model_name, content=text)
        embeddings.append(response["embedding"])

    return embeddings
