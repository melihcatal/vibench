from google.cloud import kms_v1
from google.cloud import logging_v2
from google.cloud import dlp_v2
from google.cloud import translate_v3
from vertexai.language_models import TextEmbeddingModel

def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Provides a configured Google Cloud KMS client."""
    return kms_v1.KeyManagementServiceClient()

def get_logging_client() -> logging_v2.Client:
    """Provides a configured Google Cloud Logging client."""
    return logging_v2.Client()

def get_dlp_client() -> dlp_v2.DlpServiceClient:
    """Provides a configured Google Cloud DLP client."""
    return dlp_v2.DlpServiceClient()

def get_translation_client() -> translate_v3.TranslationServiceClient:
    """Provides a configured Google Cloud Translation client."""
    return translate_v3.TranslationServiceClient()

def get_vertex_embedding_model() -> TextEmbeddingModel:
    """Provides a configured Google Cloud Vertex AI Text Embedding Model."""
    # As of recent Vertex AI SDKs, TextEmbeddingModel is initialized directly.
    return TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
