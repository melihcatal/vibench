import os
from google.cloud import aiplatform

class VertexAIModelClient:
    def __init__(self, project_id=None, location=None):
        self.project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.location = location or os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        
        aiplatform.init(project=self.project_id, location=self.location)

    def get_chat_model(self, model_name="gemini-1.5-flash-001"):
        return aiplatform.Preview.models.ChatModel.from_pretrained(model_name)

    def get_text_embedding_model(self, model_name="text-embedding-004"):
        return aiplatform.Preview.models.TextEmbeddingModel.from_pretrained(model_name)

