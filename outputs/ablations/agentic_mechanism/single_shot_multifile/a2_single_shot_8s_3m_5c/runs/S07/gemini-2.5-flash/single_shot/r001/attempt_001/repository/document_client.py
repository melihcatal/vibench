import os
from google.cloud import vision_v1, documentai_v1, translate_v3
from google.cloud import aiplatform
from google.cloud.aiplatform.language_models import TextGenerationModel, TextEmbeddingModel

def get_project_id():
    return os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT")

def get_location():
    return os.environ.get("GCP_LOCATION", "us")

def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    return vision_v1.ImageAnnotatorClient()

def get_documentai_client() -> documentai_v1.DocumentProcessorServiceClient:
    return documentai_v1.DocumentProcessorServiceClient()

def get_translation_client() -> translate_v3.TranslationServiceClient:
    return translate_v3.TranslationServiceClient()

def get_text_generation_model(model_name: str = "gemini-pro") -> TextGenerationModel:
    project_id = get_project_id()
    location = get_location()
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set for Vertex AI models.")
    aiplatform.init(project=project_id, location=location)
    return TextGenerationModel.from_pretrained(model_name)

def get_text_embedding_model(model_name: str = "text-embedding-gecko@003") -> TextEmbeddingModel:
    project_id = get_project_id()
    location = get_location()
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set for Vertex AI models.")
    aiplatform.init(project=project_id, location=location)
    return TextEmbeddingModel.from_pretrained(model_name)

DOCUMENT_AI_PROCESSOR_FORM_PARSER = "form-parser"
DOCUMENT_AI_PROCESSOR_OCR = "OCR_V1"