
import os
import boto3
from google.cloud import documentai_v1beta3 as documentai_beta
from google.cloud import documentai_v1 as documentai_v1
from google.api_core.client_options import ClientOptions
from google.cloud import translate_v3 as translate
from google.cloud import firestore
from google.cloud import aiplatform

class GoogleDocumentAIManager:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        self.documentai_client = documentai_v1.DocumentProcessorServiceClient(client_options=self.client_options)

    def get_documentai_client(self):
        return self.documentai_client

    def get_processor_name(self, processor_id: str):
        return self.documentai_client.processor_path(self.project_id, self.location, processor_id)

class AWSTextractManager:
    def __init__(self, region_name: str = None):
        self.region_name = region_name if region_name else os.getenv("AWS_REGION", "us-east-1")
        self.textract_client = boto3.client('textract', region_name=self.region_name)

    def get_textract_client(self):
        return self.textract_client

class GoogleTranslateManager:
    def __init__(self, project_id: str, location: str = "global"):
        self.project_id = project_id
        self.location = location
        self.translate_client = translate.TranslationServiceClient()

    def get_translate_client(self):
        return self.translate_client

    def get_parent(self):
        return f"projects/{self.project_id}/locations/{self.location}"

class GoogleVertexAIManager:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=self.project_id, location=self.location)

    def get_prediction_client(self):
        # Vertex AI uses a unified prediction client for various models
        return aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"})

    def get_model_name(self, publisher: str, model: str):
        return f"projects/{self.project_id}/locations/{self.location}/publishers/{publisher}/models/{model}"

class GoogleFirestoreManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        # The client automatically picks up project ID from GOOGLE_APPLICATION_CREDENTIALS
        self.db = firestore.Client(project=self.project_id)

    def get_firestore_client(self):
        return self.db

