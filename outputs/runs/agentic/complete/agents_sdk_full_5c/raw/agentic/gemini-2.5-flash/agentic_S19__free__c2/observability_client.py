import os
from google.cloud import monitoring_v3
from google.cloud import storage
from google.cloud import language_v1
from google.cloud import translate_v3
from google.cloud import aiplatform

def get_monitoring_client():
    """Provides a configured Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()

def get_storage_client():
    """Provides a configured Google Cloud Storage client."""
    return storage.Client()

def get_language_client():
    """Provides a configured Google Cloud Natural Language client."""
    return language_v1.LanguageServiceClient()

def get_translation_client():
    """Provides a configured Google Cloud Translation client."""
    return translate_v3.TranslationServiceClient()

def get_vertex_ai_model(project_id: str, location: str = "us-central1", model_name: str = "gemini-pro"):
    """Provides a configured Google Cloud Vertex AI generative model."""
    aiplatform.init(project=project_id, location=location)
    # The model name here is the concrete model identifier for Vertex AI's Gemini Pro
    return aiplatform.preview.generative_models.GenerativeModel(model_name)

# You might need to set environment variables for authentication, e.g.:
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
# export GCP_PROJECT_ID="your-gcp-project-id"
