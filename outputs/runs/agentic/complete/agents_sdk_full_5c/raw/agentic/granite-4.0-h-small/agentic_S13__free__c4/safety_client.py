# safety_client.py
"""Local configuration and client helper utilities for Text Content Safety.
Provides a thin wrapper around OpenAI's Moderation API.
"""
import os
from typing import List, Dict
import openai

class OpenAIContentSafetyClient:
    """Thin wrapper around OpenAI's moderation endpoint suitable for scoring tasks."""
    def __init__(self):
        # Set API key from environment variable (demo purpose)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        openai.api_key = api_key
        # Ensure we use the moderation model explicitly
        self.engine = "content-moderation"

    def moderate(self, texts: List[str]) -> List[Dict]:
        """Call OpenAI moderation endpoint and return raw JSON response."""
        response = openai.Moderation.create(input=texts)
        # The API returns a dict with a 'results' key containing a list of moderation results
        return response["results"]
