from typing import List, Dict, Any

# This file defines local helpers for request/response normalization,
# assuming a structure relevant to Google Gemini Embeddings API.

class EmbeddingRequest:
    """
    Helper class to structure a request for Gemini embeddings.
    """
    def __init__(self, texts: List[str], model: str = "models/text-embedding-004"):
        self.texts = texts
        self.model = model

    def to_gemini_format(self) -> Dict[str, Any]:
        """Converts the request to the format expected by Gemini's embed_content."""
        return {"content": self.texts}

class EmbeddingResponse:
    """
    Helper class to parse a response from Gemini embeddings.
    """
    def __init__(self, api_response: Any):
        self._response = api_response

    @property
    def embeddings(self) -> List[List[float]]:
        """Extracts the embedding vectors from the API response."""
        if hasattr(self._response, 'embeddings') and self._response.embeddings:
            return [e.values for e in self._response.embeddings]
        return []

    def __repr__(self):
        return f"EmbeddingResponse(num_embeddings={len(self.embeddings)})"

if __name__ == "__main__":
    # Example usage:
    sample_texts = ["First text", "Second text for embedding"]
    req = EmbeddingRequest(texts=sample_texts)
    print(f"Formatted request for Gemini: {req.to_gemini_format()}")

    # Simulate a Gemini response object for demonstration
    class MockEmbeddingValue:
        def __init__(self, values):
            self.values = values

    class MockEmbeddingObject:
        def __init__(self, embeddings_list):
            self.embeddings = [MockEmbeddingValue(v) for v in embeddings_list]

    mock_api_response = MockEmbeddingObject(embeddings_list=[
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6]
    ])

    res = EmbeddingResponse(api_response=mock_api_response)
    print(f"Parsed embeddings from response: {res.embeddings}")
