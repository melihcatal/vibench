import os
from typing import List, Dict, Any

import google.generativeai as genai

from observability_client import get_gemini_model


def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    # For embeddings, we typically use an embedding-specific model if available,
    # or a generative model that supports embedding functions.
    # The Gemini API provides `embed_content` for this purpose.

    # Configure the API key if not already done by get_gemini_model
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    embeddings = []
    for message in log_messages:
        try:
            # Use genai.embed_content for getting embeddings
            response = genai.embed_content(
                model="models/embedding-001", # Specify an embedding model
                content=message,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings.append({"original_message": message, "embedding": response["embedding"]})
        except Exception as e:
            embeddings.append({"original_message": message, "error": f"Error embedding message: {e}"})

    return embeddings
