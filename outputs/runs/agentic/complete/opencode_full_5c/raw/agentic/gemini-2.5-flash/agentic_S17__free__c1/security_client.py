import os
from google.cloud import kms_v1
from google.cloud import logging_v2
from google.cloud import dlp_v2
from google.cloud import translate_v3
from vertexai.language_models import TextEmbeddingModel


def get_kms_client():
    return kms_v1.KeyManagementServiceClient()


def get_logging_client():
    return logging_v2.LoggingServiceV2Client()


def get_dlp_client():
    return dlp_v2.DlpServiceClient()


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_embedding_model():
    # The TextEmbeddingModel is usually initialized without project details directly
    # but rather relies on the environment or explicit client initialization for auth.
    return TextEmbeddingModel.from_pretrained("text-embedding-004")
