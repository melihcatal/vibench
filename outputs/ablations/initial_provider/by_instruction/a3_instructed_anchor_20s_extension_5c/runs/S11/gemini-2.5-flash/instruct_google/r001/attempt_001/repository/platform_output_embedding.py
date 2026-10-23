from google.cloud import aiplatform
from typing import List

def platform_output_embedding(project_id: str, location: str, text: str) -> List[float]:
    """
    Generates embeddings for platform output using Google Cloud Vertex AI Embedding models.
    """
    aiplatform.init(project=project_id, location=location)
    
    # Using the latest text-embedding-004 model
    model_id = "text-embedding-004"
    
    # For models supporting predict_text_embeddings
    from vertexai.preview.language_models import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained(model_id)
    embeddings = model.get_embeddings([text])

    return embeddings[0].values
