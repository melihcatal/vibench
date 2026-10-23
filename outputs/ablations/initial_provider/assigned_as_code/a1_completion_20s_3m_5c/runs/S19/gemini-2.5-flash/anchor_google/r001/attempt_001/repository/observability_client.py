from google.cloud import monitoring_v3
from google.cloud import translate_v3
from google.cloud import storage
import google.generativeai as genai
from vertexai.preview.language_models import TextGenerationModel

def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()

def get_translate_client():
    return translate_v3.TranslationServiceClient()

def get_storage_client():
    return storage.Client()

def get_generative_model(model_name="gemini-pro"):
    # Configure genai if not already configured
    # genai.configure(api_key="YOUR_API_KEY") # This would be configured via environment variables usually
    return genai.GenerativeModel(model_name)

def get_safety_model(model_name="text-bison@001"):
    return TextGenerationModel.from_pretrained(model_name)
