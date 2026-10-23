import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language
import google.generativeai as genai

class DocumentClient:
    def __init__(self, provider_config):
        self.provider_config = provider_config

    def get_azure_document_intelligence_client(self):
        endpoint = self.provider_config.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        api_key = self.provider_config.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")
        if not endpoint or not api_key:
            raise ValueError("Azure Document Intelligence credentials not found in config.")
        return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    def get_google_document_ai_client(self):
        # Google Cloud Document AI client uses application default credentials or GOOGLE_APPLICATION_CREDENTIALS
        return documentai.DocumentProcessorServiceClient()

    def get_google_translate_client(self):
        return translate.TranslationServiceClient()

    def get_google_language_client(self):
        return language.LanguageServiceClient()

    def get_google_generative_ai_client(self):
        api_key = self.provider_config.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google API key not found in config for Generative AI.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')

    def get_vertex_ai_text_embedding_client(self):
        # Vertex AI client usually requires project and location, and handles authentication itself
        # This is a placeholder, as the actual client might need more specific setup (e.g., from vertexai.language_models)
        # For simplicity, we'll assume it's configured externally or via environment variables.
        # A more robust solution would involve explicit client initialization from vertexai.
        from vertexai.language_models import TextEmbeddingModel
        return TextEmbeddingModel.from_pretrained("text-embedding-004")
