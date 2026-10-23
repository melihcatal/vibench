from google.cloud import monitoring_v3
from google.cloud import storage
from google.cloud import translate_v2 as translate
from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel, HarmCategory, HarmBlockThreshold
import os

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.storage_client = storage.Client(project=project_id)
        self.translate_client = translate.Client(project=project_id)
        self.vertex_ai_model = TextGenerationModel.from_pretrained("text-bison@002")

    def get_monitoring_client(self):
        return self.monitoring_client

    def get_storage_client(self):
        return self.storage_client

    def get_translate_client(self):
        return self.translate_client

    def get_vertex_ai_model(self):
        return self.vertex_ai_model

def get_project_id():
    # In a real-world scenario, this might come from environment variables, metadata server, or gcloud config.
    # For this exercise, we'll use a placeholder or assume it's set in the environment.
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
