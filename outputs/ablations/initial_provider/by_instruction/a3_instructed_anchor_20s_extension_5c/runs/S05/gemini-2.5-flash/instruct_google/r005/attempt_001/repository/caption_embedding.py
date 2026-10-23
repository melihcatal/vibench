from google.cloud import aiplatform
import numpy as np
from typing import List

def get_text_embedding(texts: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """Generates embeddings for a list of text captions using Google Cloud Vertex AI Embeddings API.

    Args:
        texts: A list of text captions to embed.
        project_id: Your Google Cloud project ID.
        location: The region where your Vertex AI endpoint is located.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """

    aiplatform.init(project=project_id, location=location)

    # The TextEmbeddingModel can be initialized once and reused.
    # For this example, we initialize it within the function.
    # The model_name depends on the specific embedding model you want to use.
    # 'textembedding-gecko' is a common choice for general text embeddings.
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings_list = []
    for text in texts:
        try:
            # The predict method returns a list of TextEmbedding objects.
            # We extract the values from the first embedding (assuming single text input per call).
            embeddings = model.get_embeddings([text])
            if embeddings:
                embeddings_list.append(embeddings[0].values)
            else:
                embeddings_list.append([]) # Append empty list if no embedding is returned
        except Exception as e:
            print(f"Error generating embedding for text '{text}': {e}")
            embeddings_list.append([]) # Append empty list on error

    return embeddings_list
