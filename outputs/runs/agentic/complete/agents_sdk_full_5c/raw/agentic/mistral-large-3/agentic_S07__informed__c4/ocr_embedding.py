import os
from typing import List, Dict, Any
from openai import OpenAI


class OcrEmbedder:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_text(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        response = self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding