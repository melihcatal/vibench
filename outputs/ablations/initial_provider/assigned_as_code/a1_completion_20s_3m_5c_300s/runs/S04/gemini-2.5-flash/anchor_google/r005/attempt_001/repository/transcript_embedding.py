import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from speech_models import EmbeddingRequest, EmbeddingResult

def transcript_embedding(request: EmbeddingRequest, project_id: str, location: str = "us-central1") -> EmbeddingResult:
    aiplatform.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # Using text-embedding-004

    inputs = [TextEmbeddingInput(text, "SEMANTIC_SIMILARITY") for text in request.text_segments]
    embeddings = model.get_embeddings(inputs)
    
    return EmbeddingResult(embeddings=[embedding.values for embedding in embeddings])
