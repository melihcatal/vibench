from embeddings_client import initialize_vertexai
from embeddings_models import cosine_similarity
from vertexai.language_models import TextEmbeddingModel

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two texts using Google's Vertex AI embeddings.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        The cosine similarity score between the two text embeddings.
    """
    initialize_vertexai()
    
    # Using a specific model from Google Vertex AI
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    
    embedding1 = model.get_embeddings([text1])[0].values
    embedding2 = model.get_embeddings([text2])[0].values
    
    return cosine_similarity(embedding1, embedding2)
