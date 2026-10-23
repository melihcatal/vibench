from google.cloud import monitoring_v3
from google.cloud import translate_v3
from google.cloud import storage
import google.generativeai as genai
import os

def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()

def get_translate_client():
    return translate_v3.TranslationServiceClient()

def get_storage_client():
    return storage.Client()

def configure_generative_model(api_key: str):
    genai.configure(api_key=api_key)
    # You might want to choose a specific model here, e.g., 'gemini-pro'
    # For this example, we'll assume a default model is available or configured externally.

def get_generative_model_client(model_name: str = "gemini-pro"):
    # Ensure genai.configure has been called before this.
    return genai.GenerativeModel(model_name)
