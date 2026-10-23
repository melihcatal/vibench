import os
from google.cloud import kms_v1
from google.cloud import logging as cloud_logging
from google.cloud import language_v1
from google.cloud import translate_v2 as translate
from google.cloud import bigquery


class SecurityClientConfig:
    """Configuration holder for security clients."""
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.location_id = os.getenv("GCP_KMS_LOCATION_ID", "global")
        self.key_ring_id = os.getenv("GCP_KMS_KEY_RING_ID")
        self.key_id = os.getenv("GCP_KMS_KEY_ID")
        self.bigquery_dataset_id = os.getenv("GCP_BIGQUERY_DATASET_ID")
        self.bigquery_table_id = os.getenv("GCP_BIGQUERY_TABLE_ID")
        self.vertex_ai_project = os.getenv("GCP_VERTEX_AI_PROJECT")
        self.vertex_ai_location = os.getenv("GCP_VERTEX_AI_LOCATION")


class KmsClientWrapper:
    """Wrapper for Google Cloud KMS client with common utilities."""
    def __init__(self, config: SecurityClientConfig):
        self.config = config
        self.client = kms_v1.KeyManagementServiceClient()

    def get_crypto_key_path(self, key_id: str | None = None) -> str:
        """Returns the full resource path for a crypto key."""
        return self.client.crypto_key_path(
            self.config.project_id,
            self.config.location_id,
            self.config.key_ring_id,
            key_id if key_id else self.config.key_id,
        )

    def get_crypto_key_version_path(self, key_id: str | None = None, version_id: str | None = None) -> str:
        """Returns the full resource path for a crypto key version."""
        return self.client.crypto_key_version_path(
            self.config.project_id,
            self.config.location_id,
            self.config.key_ring_id,
            key_id if key_id else self.config.key_id,
            version_id
        )

class LoggingClientWrapper:
    """Wrapper for Google Cloud Logging client."""
    def __init__(self):
        self.client = cloud_logging.Client()

class NaturalLanguageClientWrapper:
    """Wrapper for Google Cloud Natural Language client."""
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

class TranslateClientWrapper:
    """Wrapper for Google Cloud Translation client."""
    def __init__(self):
        self.client = translate.Client()

class BigQueryClientWrapper:
    """Wrapper for Google Cloud BigQuery client."""
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
