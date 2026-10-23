import os
from google.cloud import documentai_v1 as documentai
from google.cloud import vision_v1p4beta1 as vision
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform

class DocumentClient:
    """Provides client utilities for Google Cloud Document AI, Vision, Translation, and Vertex AI."""

    def __init__(self, project_id: str, location: str = "us"):
        self.project_id = project_id
        self.location = location
        self._documentai_client = None
        self._vision_client = None
        self._translate_client = None
        self._vertex_ai_client_init = False

    @property
    def documentai_client(self) -> documentai.DocumentProcessorServiceClient:
        if self._documentai_client is None:
            self._documentai_client = documentai.DocumentProcessorServiceClient()
        return self._documentai_client

    @property
    def vision_client(self) -> vision.ImageAnnotatorClient:
        if self._vision_client is None:
            self._vision_client = vision.ImageAnnotatorClient()
        return self._vision_client

    @property
    def translate_client(self) -> translate.TranslationServiceClient:
        if self._translate_client is None:
            self._translate_client = translate.TranslationServiceClient()
        return self._translate_client

    def initialize_vertex_ai(self):
        if not self._vertex_ai_client_init:
            aiplatform.init(project=self.project_id, location=self.location)
            self._vertex_ai_client_init = True

if __name__ == '__main__':
    # Example usage
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     client_bundle = DocumentClient(project_id=project_id, location="us")
    #     doc_ai_client = client_bundle.documentai_client
    #     vision_client = client_bundle.vision_client
    #     translate_client = client_bundle.translate_client
    #     client_bundle.initialize_vertex_ai() # Initialize Vertex AI
    #     print("Clients initialized successfully.")
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    pass
