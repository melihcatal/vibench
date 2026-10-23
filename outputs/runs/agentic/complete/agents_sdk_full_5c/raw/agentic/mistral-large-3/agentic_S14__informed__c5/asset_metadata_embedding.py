import google.generativeai as genai
from typing import List, Dict, Optional
import os

class AssetMetadataEmbedder:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/embedding-001"

    def embed_metadata_and_text(self, metadata: Dict[str, str], text: str) -> List[float]:
        """Embed object metadata and extracted text for search using Google Gemini Embeddings."""
        combined_input = f"Metadata: {metadata}\nText: {text}"
        result = genai.embed_content(
            model=self.model,
            content=combined_input
        )
        return result['embedding']