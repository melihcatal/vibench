import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform


def get_documentai_client(location: str):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})


def get_translate_client():
    return translate.TranslationServiceClient()


def get_vertex_ai_model_garden_client(project_id: str, location: str):
    # Initialize Vertex AI for the given project and location
    aiplatform.init(project=project_id, location=location)
    return aiplatform
