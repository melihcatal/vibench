import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import firestore
from google.cloud import logging
import vertexai
from vertexai.preview.generative_models import GenerativeModel


def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()


def get_documentai_processor_path(project_id: str, location: str, processor_id: str):
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def get_generative_model_client(
    project_id: str, location: str, model_name: str = "gemini-1.5-flash-001"
):
    vertexai.init(project=project_id, location=location)
    return GenerativeModel(model_name)


def get_translation_client():
    return translate.TranslationServiceClient()


def get_firestore_client(project_id: str):
    return firestore.Client(project=project_id)


def get_logging_client():
    return logging.Client()
