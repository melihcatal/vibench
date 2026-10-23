import os
import json
import requests
from document_models import DocumentResponse

class OCREmbedder:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.endpoint = "https://api.dashscope.ai/v1/embeddings"

    def embed_text(self, text: str) -> List[float]:
        payload = {
            "model": "text-embedding-001",
            "input": [text]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        resp = requests.post(self.endpoint, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        # DashScope returns embeddings under data[0][\"embedding\"]
        return result["data"][0]["embedding"]

    def embed_document(self, doc: DocumentResponse) -> List[float]:
        return self.embed_text(doc["text"])

if __name__ == "__main__":
    from extract_text import ExtractText
    extractor = ExtractText()
    doc = extractor.extract("sample.jpg")
    embedder = OCREmbedder()
    vector = embedder.embed_document(doc)
    print(vector)
