import boto3

def get_transcribe_client(region_name):
    return boto3.client("transcribe", region_name=region_name)

def get_translate_client(project_id, location="global"):
    from google.cloud import translate_v3beta1 as translate
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    return client, parent

def get_language_client():
    from google.cloud import language_v1
    return language_v1.LanguageServiceClient()

def get_vertex_ai_prediction_client(project_id, location):
    from google.cloud import aiplatform
    aiplatform.init(project=project_id, location=location)
    return aiplatform.gapic.PredictionServiceClient()

def get_vertex_ai_embedding_model(model_name):
    from vertexai.language_models import TextEmbeddingModel
    return TextEmbeddingModel.from_pretrained(model_name)
