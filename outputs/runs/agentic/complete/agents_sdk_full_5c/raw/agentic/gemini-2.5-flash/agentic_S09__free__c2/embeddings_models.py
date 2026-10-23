from typing import List, Dict, Any, Union

class EmbeddingResult:
    """A simple class to represent an embedding result from a service like Vertex AI."""
    def __init__(self, values: List[float], statistics: Dict[str, Any] = None):
        self.values = values
        self.statistics = statistics if statistics is not None else {}

    @classmethod
    def from_vertex_ai_response(cls, vertex_ai_embedding_object: Any) -> 'EmbeddingResult':
        """Converts a Vertex AI Embedding object to an EmbeddingResult.
        The Any type is used to avoid a direct google.cloud.aiplatform import here
        to keep this file purely for local model definitions/helpers.
        """
        return cls(values=list(vertex_ai_embedding_object.values), statistics={})

    def to_dict(self) -> Dict[str, Union[List[float], Dict[str, Any]]]:
        """Converts the EmbeddingResult to a dictionary."""
        return {"values": self.values, "statistics": self.statistics}

    @classmethod
    def from_dict(cls, data: Dict[str, Union[List[float], Dict[str, Any]]]) -> 'EmbeddingResult':
        """Creates an EmbeddingResult from a dictionary."""
        return cls(values=data["values"], statistics=data.get("statistics", {}))


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector to a unit vector (L2 normalization).

    Args:
        embedding: The embedding vector to normalize.

    Returns:
        The L2-normalized embedding vector.
    """
    norm = sum(x**2 for x in embedding)**0.5
    if norm == 0:
        return embedding # Avoid division by zero
    return [x / norm for x in embedding]

if __name__ == '__main__':
    # Example usage:
    dummy_embedding_values = [0.1, 0.2, 0.3]
    embedding_obj = EmbeddingResult(values=dummy_embedding_values)
    # print(f"Original embedding: {embedding_obj.values}")
    # print(f"Normalized embedding: {normalize_embedding(embedding_obj.values)}")

    # Example of conversion from a mock Vertex AI-like object
    class MockVertexAIEmbedding:
        def __init__(self, values):
            self.values = values

    mock_vertex_embedding = MockVertexAIEmbedding(values=[0.5, 0.5, 0.707])
    converted_embedding = EmbeddingResult.from_vertex_ai_response(mock_vertex_embedding)
    # print(f"Converted from mock Vertex AI: {converted_embedding.values}")
