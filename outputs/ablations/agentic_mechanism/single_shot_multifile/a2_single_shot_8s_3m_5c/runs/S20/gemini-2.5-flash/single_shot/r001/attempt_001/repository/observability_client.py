import os
from google.cloud import logging, logging_v2
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel

# Google Cloud Logging clients
_logging_client = None
_logging_v2_client = None

def get_logging_client():
    global _logging_client
    if _logging_client is None:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS or default ADC is set
        _logging_client = logging.Client()
    return _logging_client

def get_logging_v2_client():
    global _logging_v2_client
    if _logging_v2_client is None:
        # Used for list_log_entries, which is in logging_v2 service
        _logging_v2_client = logging_v2.LoggingServiceV2Client()
    return _logging_v2_client

# Google Cloud Vertex AI clients/models
_generative_model_instance = None
_embedding_model_instance = None

def get_generative_model(model_name: str = "gemini-pro"):
    global _generative_model_instance
    if _generative_model_instance is None or _generative_model_instance.model_name != model_name:
        # vertexai.init() should be called once, typically at application start
        # For this example, we assume it's initialized elsewhere or relies on default project/location
        _generative_model_instance = GenerativeModel(model_name)
    return _generative_model_instance

def get_embedding_model(model_name: str = "text-embedding-004"):
    global _embedding_model_instance
    if _embedding_model_instance is None or _embedding_model_instance.model_name != model_name:
        # Assumes vertexai.init() is called
        _embedding_model_instance = TextEmbeddingModel.from_pretrained(model_name)
    return _embedding_model_instance
