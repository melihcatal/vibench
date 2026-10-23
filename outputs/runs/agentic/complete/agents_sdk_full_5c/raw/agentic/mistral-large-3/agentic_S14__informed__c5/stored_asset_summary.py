import google.generativeai as genai
from typing import Optional
import os

class StoredAssetSummarizer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def summarize_content(self, content: str) -> str:
        """Summarize content extracted from a stored asset using Google Gemini API."""
        response = self.model.generate_content(
            f"Summarize the following content in a concise manner:\n\n{content}"
        )
        return response.text