from google.cloud import vision_v1p4beta1 as vision
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3beta1 as translate
from google.cloud import language_v1 as language
from google.cloud import aiplatform


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_language_client():
    return language.LanguageServiceClient()


def get_vertex_ai_prediction_client():
    return aiplatform.gapic.PredictionServiceClient()
