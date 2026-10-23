import os
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language
from google.cloud import aiplatform

class DocumentClient:
    def __init__(self, project_id: str, location: str = "us"):
        self.project_id = project_id
        self.location = location

    def get_documentai_client(self):
        return documentai.DocumentProcessorServiceClient()

    def get_translate_client(self):
        return translate.TranslationServiceClient()

    def get_language_client(self):
        return language.LanguageServiceClient()

    def get_vertex_ai_text_embedding_client(self):
        # Initialize Vertex AI for embeddings
        aiplatform.init(project=self.project_id, location=self.location)
        return aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"}
        )

# Helper to get project ID from environment or a default
def get_project_id():
    return os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
