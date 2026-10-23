from google.cloud import vision
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1
from google.cloud import aiplatform

def get_document_vision_client():
    return vision.ImageAnnotatorClient()

def get_document_processor_client():
    return documentai.DocumentProcessorServiceClient()

def get_translation_client():
    return translate.TranslationServiceClient()

def get_language_client():
    return language_v1.LanguageServiceClient()

def get_embedding_model(project_id: str, location: str, model_name: str = "text-embedding-004"):
    aiplatform.init(project=project_id, location=location)
    return aiplatform.TextEmbeddingModel.from_pretrained(model_name)
