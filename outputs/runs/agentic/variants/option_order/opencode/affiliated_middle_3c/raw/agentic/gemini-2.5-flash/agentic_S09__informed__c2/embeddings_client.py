import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class EmbeddingsClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/embedding-001"

    def embed_text(self, text: str) -> list[float]:
        result = genai.embed_content(model=self.model, content=text)
        return result["""embedding"""]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        result = genai.embed_content(model=self.model, content=texts)
        return [item["""embedding"""] for item in result["""embeddings"""]]
