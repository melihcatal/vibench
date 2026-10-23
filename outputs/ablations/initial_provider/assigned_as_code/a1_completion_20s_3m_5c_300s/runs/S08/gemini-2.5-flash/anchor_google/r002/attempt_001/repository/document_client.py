import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel

def get_documentai_client(location: str):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )

def get_translation_client():
    return translate.TranslationServiceClient()

def get_firestore_client(project_id: str):
    return firestore.Client(project=project_id)

def get_vertex_ai_model(project_id: str, location: str, model_name: str = "gemini-pro"):
    vertexai.init(project=project_id, location=location)
    return GenerativeModel(model_name)

