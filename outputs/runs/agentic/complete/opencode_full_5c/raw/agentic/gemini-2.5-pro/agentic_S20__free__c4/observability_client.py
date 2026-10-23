import os
from google.cloud import logging
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel


def get_logging_client():
    project_id = os.environ.get("GCP_PROJECT_ID")
    return logging.Client(project=project_id)


def get_logger(name="app_logger"):
    client = get_logging_client()
    return client.logger(name)


def get_vertex_ai_client():
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)
    return aiplatform


def get_generative_model_client(model_name="gemini-1.5-flash-001"):
    get_vertex_ai_client()
    return GenerativeModel(model_name)


def get_embedding_model_client(model_name="textembedding-gecko@003"):
    get_vertex_ai_client()
    return TextEmbeddingModel.from_pretrained(model_name)
