import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_palm_model() -> TextGenerationModel:
    return TextGenerationModel.from_pretrained("text-bison@002") # Provider-specific model ID

def get_embedding_model() -> TextEmbeddingModel:
    return TextEmbeddingModel.from_pretrained("text-embedding-004") # Provider-specific model ID
