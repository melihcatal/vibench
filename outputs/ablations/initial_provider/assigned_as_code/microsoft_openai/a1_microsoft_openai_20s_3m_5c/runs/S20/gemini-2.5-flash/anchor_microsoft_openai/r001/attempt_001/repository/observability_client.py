import os
from google.cloud import logging_v2
from google.cloud import translate_v3beta1
from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel, TextSafetyModel

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.logging_client = logging_v2.Client(project=project_id)
        self.log_name = os.environ.get("GOOGLE_CLOUD_LOG_NAME", "application-logs")
        self.translate_client = translate_v3beta1.TranslationServiceClient()
        # Initialize Vertex AI models
        self.text_generation_model = TextGenerationModel.from_pretrained("text-bison@002")
        self.text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        self.text_safety_model = TextSafetyModel.from_pretrained("text-bison-safety")

    def get_logger(self):
        return self.logging_client.logger(self.log_name)

    def get_logging_client(self):
        return self.logging_client
    
    def get_translate_client(self):
        return self.translate_client

    def get_text_generation_model(self):
        return self.text_generation_model

    def get_text_embedding_model(self):
        return self.text_embedding_model
    
    def get_text_safety_model(self):
        return self.text_safety_model
