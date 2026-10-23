import os
import google.generativeai as genai
from typing import List

class ModerationEmbedder:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004" # A concrete embedding model

    def embed_rationale(self, rationale_text: str) -> List[float]:
        """
        Generates an embedding for the given moderation rationale text.
        """
        result = genai.embed_content(
            model=self.model_name,
            content=rationale_text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result["embedding"]
