import os
from google.cloud import monitoring_v3
from google.cloud import translate_v3
from google.cloud import language_v1
from google.cloud import storage


class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.language_client = language_v1.LanguageServiceClient()
        self.storage_client = storage.Client(project=project_id)

    def get_monitoring_client(self):
        return self.monitoring_client

    def get_translate_client(self):
        return self.translate_client

    def get_language_client(self):
        return self.language_client

    def get_storage_client(self):
        return self.storage_client
