import os
from typing import List
from document_models import LayoutBlock

class VectorStoreClient:
    def __init__(self):
        self.endpoint = os.getenv("SUPPORTED_EMBEDDING_STORE_ENDPOINT")
        self.api_key = os.getenv("SUPPORTED_EMBEDDING_STORE_API_KEY")

    def upsert_document(self, doc_id: str, text: str, embedding: bytes):
        """Store a document's section with its embedding for semantic retrieval."""
        url = f"{self.endpoint}/upsert"
        payload = {
          "id": doc_id,
          "text": text,
          "vector": [float(x) for x in embedding.decode('latin1')]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()

    def query(self, query_text: str) -> List[str]:
        """Retrieve top-k similar stored sections based on embedding similarity."""
        url = f"{self.endpoint}/query"
        payload = {
            "text": query_text,
            "top_k": 5
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data['results']

# Example usage (not executed here)
# store = VectorStoreClient()
# store.upsert_document('doc_123', normalized_text, embedding_bytes)
# similar_texts = store.query('who is the signatory?')
