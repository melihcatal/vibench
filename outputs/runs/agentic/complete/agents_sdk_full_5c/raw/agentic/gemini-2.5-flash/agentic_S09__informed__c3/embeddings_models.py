from typing import List, Dict, Any

# This file can be used for defining Pydantic models for request/response
# or for normalizing outputs, but for the Google Gemini SDK, the direct
# response parsing is often sufficient.
# We'll define a simple structure for demonstration.

class EmbeddingResponse:
    """
    A simple wrapper for embedding responses from Google Gemini.
    """
    def __init__(self, raw_response: Dict[str, Any]):
        self._raw_response = raw_response
        self.embeddings = self._parse_embeddings()

    def _parse_embeddings(self) -> List[List[float]]:
        if 'embedding' in self._raw_response:
            return [self._raw_response['embedding']]
        elif 'embeddings' in self._raw_response:
            return [item['embedding'] for item in self._raw_response['embeddings']]
        return []

    def get_first_embedding(self) -> List[float]:
        if self.embeddings:
            return self.embeddings[0]
        return []

    def get_all_embeddings(self) -> List[List[float]]:
        return self.embeddings

    @property
    def raw_response(self) -> Dict[str, Any]:
        return self._raw_response

class EmbeddingRequest:
    """
    A simple model for structuring an embedding request.
    This might be more useful if building a REST client directly.
    """
    def __init__(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT"):
        self.texts = texts
        self.task_type = task_type
        self.model = "models/embedding-001" # Google Gemini specific model

    def to_json(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "content": self.texts,
            "task_type": self.task_type
        }

if __name__ == '__main__':
    # Example raw responses from genai.GenerativeModel.embed_content
    single_embedding_raw = {
        'embedding': [0.1, 0.2, 0.3],
        'version': 1
    }
    batch_embeddings_raw = {
        'embeddings': [
            {'embedding': [0.4, 0.5, 0.6]},
            {'embedding': [0.7, 0.8, 0.9]}
        ],
        'version': 1
    }

    single_resp = EmbeddingResponse(single_embedding_raw)
    print(f"Parsed single embedding: {single_resp.get_first_embedding()}")

    batch_resp = EmbeddingResponse(batch_embeddings_raw)
    print(f"Parsed batch embeddings: {batch_resp.get_all_embeddings()}")

    request_example = EmbeddingRequest(
        texts=["hello", "world"],
        task_type="RETRIEVAL_QUERY"
    )
    print(f"Example request JSON: {request_example.to_json()}")
