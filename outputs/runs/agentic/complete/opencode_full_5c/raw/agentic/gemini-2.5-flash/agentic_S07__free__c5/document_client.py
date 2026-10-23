import os
from google.cloud import vision
from google.cloud import documentai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language
from google.cloud import aiplatform


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_language_client():
    return language.LanguageServiceClient()


def get_vertex_ai_text_embedding_client():
    # Initialize Vertex AI for text embeddings. Ensure GOOGLE_CLOUD_PROJECT is set.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # The client needs to be initialized with the project and location
    # For text embeddings, we typically use the `text-embedding-004` model
    # but the client itself is for AI Platform general services.
    # The actual embedding call will specify the model.
    # For simplicity, we are returning a client that can be used to call the Vertex AI APIs
    # and the specific model will be passed in the embedding function.
    aiplatform.init(project=project_id, location="us-central1")
    return aiplatform.gapic.PredictionServiceClient()
