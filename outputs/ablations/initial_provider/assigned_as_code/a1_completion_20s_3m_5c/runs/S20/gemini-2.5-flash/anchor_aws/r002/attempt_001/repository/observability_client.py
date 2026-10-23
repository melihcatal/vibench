import boto3
from google.cloud import translate_v3, aiplatform

class ObservabilityClient:
    def __init__(self, region_name: str, project_id: str, location: str):
        self.logs_client = boto3.client("logs", region_name=region_name)
        self.translate_client = translate_v3.TranslationServiceClient()
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)

    def get_logs_client(self):
        return self.logs_client

    def get_translate_client(self):
        return self.translate_client

    def get_aiplatform_model(self, model_name: str):
        return aiplatform.LanguageModel.from_pretrained(model_name)

    def get_text_embedding_model(self, model_name: str):
        return aiplatform.TextEmbeddingModel.from_pretrained(model_name)
