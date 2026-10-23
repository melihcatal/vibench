from typing import List, Dict, Any

# Define a simple Pydantic-like structure for clarity, though not strictly Pydantic itself.
# In a real application, you might use Pydantic for robust validation.

class EmbeddingRequest:
    """
    Represents a request payload for the Google Cloud Vertex AI embedding API.
    """
    def __init__(self, content: str):
        self.content = content

    def to_instance(self) -> Dict[str, str]:
        """Converts the request to the Vertex AI 'instance' format."""
        return {"content": self.content}

class EmbeddingResponse:
    """
    Represents a normalized response from the Google Cloud Vertex AI embedding API.
    """
    def __init__(self, values: List[float], statistics: Dict[str, Any] = None):
        self.values = values
        self.statistics = statistics if statistics is not None else {}

    @classmethod
    def from_prediction_dict(cls, prediction: Dict[str, Any]) -> 'EmbeddingResponse':
        """
        Creates an EmbeddingResponse from a Vertex AI prediction dictionary.
        Expected format: {'embeddings': {'values': [...], 'statistics': {...}}}
        """
        embeddings_data = prediction.get('embeddings', {})
        values = embeddings_data.get('values', [])
        statistics = embeddings_data.get('statistics', {})
        return cls(values=values, statistics=statistics)

def normalize_embeddings_response(api_response: Any) -> List[EmbeddingResponse]:
    """
    Normalizes the full API response from Vertex AI embedding prediction.
    """
    normalized_results = []
    if hasattr(api_response, 'predictions') and api_response.predictions:
        for pred_dict in api_response.predictions:
            normalized_results.append(EmbeddingResponse.from_prediction_dict(pred_dict))
    return normalized_results

if __name__ == "__main__":
    # Example Usage
    print("Demonstrating EmbeddingRequest:")
    req = EmbeddingRequest(content="Sample text for embedding.")
    print(f"Request instance: {req.to_instance()}")

    print("\nDemonstrating EmbeddingResponse and normalization:")
    # Simulate a raw API response structure from Vertex AI
    mock_api_prediction = {
        "predictions": [
            {
                "embeddings": {
                    "values": [0.1, 0.2, 0.3, 0.4, 0.5],
                    "statistics": {"token_count": 5, "truncated": False}
                }
            },
            {
                "embeddings": {
                    "values": [0.5, 0.4, 0.3, 0.2, 0.1],
                    "statistics": {"token_count": 6, "truncated": False}
                }
            }
        ]
    }
    
    # Create a mock object with a 'predictions' attribute to simulate aiplatform.models.Prediction
    class MockPredictionResponse:
        def __init__(self, predictions):
            self.predictions = predictions
            
    mock_response_obj = MockPredictionResponse(mock_api_prediction["predictions"])

    normalized_responses = normalize_embeddings_response(mock_response_obj)

    for i, res in enumerate(normalized_responses):
        print(f"Embedding {i+1} values (first 3): {res.values[:3]}...")
        print(f"Embedding {i+1} statistics: {res.statistics}")