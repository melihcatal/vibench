import os
from google.cloud import logging
import vertexai
from google.cloud import translate_v3 as translate

def get_gcp_project_id():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

def get_logging_client():
    return logging.Client(project=get_gcp_project_id())

def get_vertex_ai_model(model_name: str):
    project_id = get_gcp_project_id()
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)
    from vertexai.preview.generative_models import GenerativeModel
    return GenerativeModel(model_name)

def get_vertex_ai_embedding_model(model_name: str):
    project_id = get_gcp_project_id()
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)
    from vertexai.language_models import TextEmbeddingModel
    return TextEmbeddingModel.from_pretrained(model_name)

def get_translation_client():
    return translate.TranslationServiceClient()