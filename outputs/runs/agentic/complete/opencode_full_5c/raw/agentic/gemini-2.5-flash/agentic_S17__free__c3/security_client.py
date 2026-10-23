import os
import base64
from google.cloud import kms_v1
from google.cloud import dlp_v2
from google.cloud import logging_v2
from google.cloud import translate
from vertexai.language_models import TextEmbeddingModel

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
KMS_LOCATION = os.environ.get("KMS_LOCATION", "global")


def get_kms_client():
    return kms_v1.KeyManagementServiceClient()


def get_dlp_client():
    return dlp_v2.DlpServiceClient()


def get_logging_client():
    return logging_v2.LoggingServiceV2Client()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_embedding_model():
    return TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
