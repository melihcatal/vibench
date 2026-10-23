import os
from google.cloud import kms_v1
from google.cloud import logging_v2
from google.cloud import dlp_v2
from google.cloud import translate_v3
from google.cloud import aiplatform


class SecurityClient:
    def __init__(self):
        self.kms_client = kms_v1.KeyManagementServiceClient()
        self.logging_client = logging_v2.LoggingClient()
        self.dlp_client = dlp_v2.DlpServiceClient()
        self.translate_client = translate_v3.TranslationServiceClient()
        aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"))
        self.prediction_client = aiplatform.gapic.PredictionServiceClient()

    def get_kms_key_path(self, key_config):
        return self.kms_client.crypto_key_path(
            key_config.project_id,
            key_config.location_id,
            key_config.key_ring_id,
            key_config.key_id,
        )

    def get_kms_key_version_path(self, key_config):
        if key_config.key_version_id:
            return self.kms_client.crypto_key_version_path(
                key_config.project_id,
                key_config.location_id,
                key_config.key_ring_id,
                key_config.key_id,
                key_config.key_version_id,
            )
        return (
            self.get_kms_key_path(key_config) + "/cryptoKeyVersions/1"
        )  # Default to version 1 if not specified
