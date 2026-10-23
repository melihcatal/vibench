import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.api_core.client_options import ClientOptions
import google.generativeai as genai


class DocumentClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us" or "eu"

    def get_documentai_client(self):
        opts = ClientOptions(api_endpoint=f"{self.location}-documentai.googleapis.com")
        return documentai.DocumentProcessorServiceClient(client_options=opts)

    def get_translation_client(self):
        return translate.TranslationServiceClient()

    def get_gemini_client(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        return genai
