from typing import List, Dict, Any

class EmbeddingRequest:
    """Represents a request payload for the embeddings API."""
    def __init__(self, texts: List[str], model: str = "models/embedding-001", task_type: str = "RETRIEVAL_DOCUMENT"):
        self.texts = texts
        self.model = model
        self.task_type = task_type

    def to_gemini_content_format(self) -> List[Dict[str, Any]]:
        """Converts texts to the format expected by genai.embed_content."""
        return self.texts # For simple string lists, it's just the list itself

class EmbeddingResponse:
    """Represents a normalized response from the embeddings API."""
    def __init__(self, embeddings_data: List[List[float]]):
        self.embeddings = embeddings_data

    @classmethod
    def from_gemini_response(cls, api_response: Dict[str, Any]) -> 'EmbeddingResponse':
        """Parses a Gemini API response into a normalized EmbeddingResponse."""
        extracted_embeddings = []
        if 'embeddings' in api_response:
            extracted_embeddings = api_response['embeddings']
        return cls(extracted_embeddings)

    def get_embeddings(self) -> List[List[float]]:
        """Returns the list of embedding vectors."""
        return self.embeddings

