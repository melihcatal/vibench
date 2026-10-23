# This file defines local request, response, and normalization helpers
# for Direct Embeddings API, specifically for Google Cloud Vertex AI.

from typing import List, Dict, Any

class VertexAITextEmbeddingRequest:
    """Represents a request payload for Vertex AI text embedding."""
    def __init__(self, content: str):
        self.instances = [{"content": content}]

    @classmethod
    def from_texts(cls, texts: List[str]):
        """Creates a request object for a batch of texts."""
        instance = cls("") # Create a dummy instance
        instance.instances = [{"content": text} for text in texts]
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """Converts the request to a dictionary suitable for API calls."""
        return {"instances": self.instances}

class VertexAITextEmbeddingResponse:
    """Represents a normalized response from Vertex AI text embedding."""
    def __init__(self, api_response: Dict[str, Any]):
        self._response = api_response

    def get_embeddings(self) -> List[List[float]]:
        """Extracts the embedding vectors from the API response."""
        embeddings = []
        if 'predictions' in self._response:
            for prediction in self._response['predictions']:
                if 'embeddings' in prediction and 'values' in prediction['embeddings']:
                    embeddings.append(prediction['embeddings']['values'])
        return embeddings

if __name__ == '__main__':
    # Example Usage
    single_text_req = VertexAITextEmbeddingRequest(content="Hello, AI!")
    print(f"Single text request: {single_text_req.to_dict()}")

    batch_texts = ["First sentence.", "Second sentence."]
    batch_text_req = VertexAITextEmbeddingRequest.from_texts(batch_texts)
    print(f"Batch text request: {batch_text_req.to_dict()}")

    # Simulate an API response
    mock_api_response = {
        "predictions": [
            {"embeddings": {"values": [0.1, 0.2, 0.3], "statistics": {"token_count": 3}}},
            {"embeddings": {"values": [0.4, 0.5, 0.6], "statistics": {"token_count": 2}}}
        ],
        "metadata": {}
    }
    response_obj = VertexAITextEmbeddingResponse(mock_api_response)
    print(f"Extracted embeddings: {response_obj.get_embeddings()}")
