from google.cloud import logging_v2, translate_v3, bigquery_data_transfer_v1
from vertexai.preview.generative_models import GenerativeModel
import os

def get_logging_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return logging_v2.Client(project=project_id)

def get_generative_model(model_name="gemini-pro"):
    return GenerativeModel(model_name)

def get_translate_client():
    return translate_v3.TranslationServiceClient()
