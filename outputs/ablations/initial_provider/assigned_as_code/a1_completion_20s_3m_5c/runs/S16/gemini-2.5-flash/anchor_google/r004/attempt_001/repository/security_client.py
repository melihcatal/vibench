from google.cloud import secretmanager
from google.cloud import language_v2
from google.cloud import translate_v3 as translate
from vertexai.language_models import TextEmbeddingModel


def get_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()

def get_natural_language_client():
    return language_v2.LanguageServiceClient()

def get_embedding_model():
    return TextEmbeddingModel.from_pretrained("text-embedding-004")

def get_translation_client():
    return translate.TranslationServiceClient()
