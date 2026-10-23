from google.cloud import logging_v2
from google.cloud import language_v1
from google.cloud import translate_v2 as translate
import vertexai
from google.cloud import aiplatform

class ObservabilityClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.logging_client = logging_v2.Client(project=self.project_id)
        self.natural_language_client = language_v1.LanguageServiceClient()
        self.translate_client = translate.Client(project=self.project_id)
        vertexai.init(project=self.project_id, location="us-central1")
        self.embedding_model = aiplatform.get_model("textembedding-gecko@003")

    def get_logging_client(self):
        return self.logging_client

    def get_natural_language_client(self):
        return self.natural_language_client

    def get_translate_client(self):
        return self.translate_client

    def get_embedding_model(self):
        return self.embedding_model
