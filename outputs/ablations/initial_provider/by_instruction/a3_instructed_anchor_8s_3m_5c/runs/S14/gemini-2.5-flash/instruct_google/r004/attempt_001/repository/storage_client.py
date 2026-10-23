from google.cloud import storage
from google.cloud import vision
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language
from google.cloud import aiplatform

def get_storage_client():
    """Returns a Google Cloud Storage client."""
    return storage.Client()

def get_vision_client():
    """Returns a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()

def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate.TranslationServiceClient()

def get_language_client():
    """Returns a Google Cloud Natural Language client."""
    return language.LanguageServiceClient()

def get_aiplatform_text_embedding_client():
    """Returns a Google Cloud AI Platform Text Embedding client."""
    # aiplatform.init sets the project and location for subsequent AI Platform API calls.
    # Replace with your actual project ID and desired location.
    # For this example, we'll assume project and location are set via environment variables
    # or gcloud default configuration. If not, uncomment and set them explicitly:
    # aiplatform.init(project='YOUR_PROJECT_ID', location='YOUR_LOCATION')
    # The TextEmbeddingModel is initialized without project/location if already set globally
    # or if using a default model that doesn't require explicit project/location.
    # For a specific model, you might need to specify the model_id directly.
    # For text-embedding-004, it's generally available and doesn't require explicit project/location for basic usage.
    return aiplatform.gapic.PredictionServiceClient()

def get_aiplatform_text_model_client(model_name: str):
    """Returns a Google Cloud AI Platform Text Generation client for a specific model."""
    # Similar to embedding client, project and location can be set globally or via env vars.
    # For example, text-bison@002 or gemini-pro
    return aiplatform.gapic.PredictionServiceClient()

