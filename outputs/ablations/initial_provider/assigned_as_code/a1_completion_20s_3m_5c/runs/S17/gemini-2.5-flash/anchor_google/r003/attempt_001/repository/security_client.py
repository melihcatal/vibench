import os
from google.cloud import kms
from google.cloud import language_v1
from google.cloud import translate_v3
from google.cloud import logging_v2
from google.cloud import aiplatform


class SecurityClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self._kms_client = None
        self._language_client = None
        self._translate_client = None
        self._logging_client = None
        self._vertex_ai_client_initialized = False

    def get_kms_client(self):
        if self._kms_client is None:
            self._kms_client = kms.KeyManagementServiceClient()
        return self._kms_client

    def get_language_client(self):
        if self._language_client is None:
            self._language_client = language_v1.LanguageServiceClient()
        return self._language_client

    def get_translate_client(self):
        if self._translate_client is None:
            self._translate_client = translate_v3.TranslationServiceClient()
        return self._translate_client

    def get_logging_client(self):
        if self._logging_client is None:
            self._logging_client = logging_v2.LoggingServiceV2Client()
        return self._logging_client

    def get_vertex_ai_text_embedding_model(self):
        if not self._vertex_ai_client_initialized:
            aiplatform.init(project=self.project_id, location=self.location)
            self._vertex_ai_client_initialized = True
        return aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")


def get_kms_key_path(project_id: str, location: str, key_ring: str, key_id: str) -> str:
    return kms.KeyManagementServiceClient().crypto_key_path(project_id, location, key_ring, key_id)

def get_kms_key_version_path(project_id: str, location: str, key_ring: str, key_id: str, version_id: str) -> str:
    return kms.KeyManagementServiceClient().crypto_key_version_path(project_id, location, key_ring, key_id, version_id)

