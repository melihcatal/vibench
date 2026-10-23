import os
from google.cloud import kms_v1
from google.cloud import translate_v3
import google.generativeai as genai


class KmsClient:
    def __init__(self):
        self.client = kms_v1.KeyManagementServiceClient()


class TranslationClient:
    def __init__(self):
        self.client = translate_v3.TranslationServiceClient()


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")


class GeminiEmbeddingClient:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
