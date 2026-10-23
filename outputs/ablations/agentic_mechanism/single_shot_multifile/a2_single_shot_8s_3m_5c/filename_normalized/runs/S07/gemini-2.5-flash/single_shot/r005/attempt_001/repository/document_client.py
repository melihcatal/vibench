import os
from google.cloud import documentai_v1 as documentai
from google.cloud import vision_v1p4beta1 as vision
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform_v1 as aiplatform

_document_ai_client = None
_vision_client = None
_translate_client = None
_aiplatform_prediction_client = None

def get_document_ai_client():
    global _document_ai_client
    if _document_ai_client is None:
        _document_ai_client = documentai.DocumentProcessorServiceClient()
    return _document_ai_client

def get_vision_client():
    global _vision_client
    if _vision_client is None:
        _vision_client = vision.ImageAnnotatorClient()
    return _vision_client

def get_translation_client():
    global _translate_client
    if _translate_client is None:
        _translate_client = translate.TranslationServiceClient()
    return _translate_client

def get_aiplatform_prediction_client():
    global _aiplatform_prediction_client
    if _aiplatform_prediction_client is None:
        _aiplatform_prediction_client = aiplatform.PredictionServiceClient(client_options={
            "api_endpoint": f"{os.environ.get('GOOGLE_CLOUD_LOCATION')}-aiplatform.googleapis.com"
        })
    return _aiplatform_prediction_client
