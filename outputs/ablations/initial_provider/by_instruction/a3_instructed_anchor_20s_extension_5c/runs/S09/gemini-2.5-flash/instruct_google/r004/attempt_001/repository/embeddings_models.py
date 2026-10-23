from typing import Any, Dict, List

class EmbeddingsModels:
    """Defines local request, response, and normalization helpers for Direct Embeddings API.
    """
    @staticmethod
    def prepare_instances(texts: List[str]) -> List[Dict[str, Any]]:
        """Prepares a list of text strings into the format expected by the Vertex AI embeddings API.

        Args:
            texts: A list of text strings.

        Returns:
            A list of dictionaries, each representing an instance for the API.
        """
        return [{"content": text} for text in texts]

    @staticmethod
    def parse_response(response: Any) -> List[List[float]]:
        """Parses the response from the Vertex AI embeddings API to extract embedding vectors.

        Args:
            response: The raw response object from the API.

        Returns:
            A list of embedding vectors, where each vector is a list of floats.
        """
        embeddings = []
        for prediction in response.predictions:
            embeddings.append(prediction["embeddings"]["values"])
        return embeddings
