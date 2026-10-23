from typing import List, Dict, Any

class EmbeddingResult:
    """A simple class to hold an embedding vector and its source text.

    This serves as a local helper for standardizing embedding responses,
    especially from providers like Google Cloud Vertex AI's textembedding-gecko@003.
    """
    def __init__(self, text: str, embedding: List[float]):
        self.text = text
        self.embedding = embedding

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "embedding": self.embedding}

def normalize_vertex_embedding_response(texts: List[str], vertex_embeddings) -> List[EmbeddingResult]:
    """Normalizes Vertex AI TextEmbeddingModel response into a list of EmbeddingResult objects.

    Args:
        texts: The original list of texts that were embedded.
        vertex_embeddings: The raw response from Vertex AI's get_embeddings method.

    Returns:
        A list of EmbeddingResult objects.
    """
    normalized_results = []
    for i, text in enumerate(texts):
        if i < len(vertex_embeddings):
            embedding_values = vertex_embeddings[i].values
            normalized_results.append(EmbeddingResult(text, embedding_values))
    return normalized_results

if __name__ == '__main__':
    # Example usage (mocking Vertex AI response):
    # from types import SimpleNamespace
    # mock_vertex_embedding_obj1 = SimpleNamespace(values=[0.1, 0.2, 0.3])
    # mock_vertex_embedding_obj2 = SimpleNamespace(values=[0.4, 0.5, 0.6])
    # mock_vertex_embeddings_response = [mock_vertex_embedding_obj1, mock_vertex_embedding_obj2]
    # original_texts = ["text1", "text2"]
    # normalized = normalize_vertex_embedding_response(original_texts, mock_vertex_embeddings_response)
    # for res in normalized:
    #     print(f"Text: {res.text}, Embedding (first 2): {res.embedding[:2]}...")
    pass
