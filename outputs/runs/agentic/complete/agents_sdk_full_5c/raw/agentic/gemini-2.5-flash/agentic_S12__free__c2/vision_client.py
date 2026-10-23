from google.cloud import vision
from google.cloud import translate_v3 as translate
import vertexai
from google.cloud import storage

def get_vision_client():
    """Returns a Google Cloud Vision API client."""
    return vision.ImageAnnotatorClient()

def get_translation_client():
    """Returns a Google Cloud Translation API client."""
    return translate.TranslationServiceClient()

def initialize_vertexai(project_id: str, location: str):
    """Initializes Vertex AI for generative models."""
    vertexai.init(project=project_id, location=location)

def get_storage_client():
    """Returns a Google Cloud Storage client."""
    return storage.Client()
