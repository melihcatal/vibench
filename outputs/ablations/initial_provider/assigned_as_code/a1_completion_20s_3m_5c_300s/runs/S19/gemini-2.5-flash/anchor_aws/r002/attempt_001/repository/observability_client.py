import boto3
from google.cloud import storage, translate_v2 as translate, aiplatform

def get_cloudwatch_client(region_name: str):
    return boto3.client("cloudwatch", region_name=region_name)

def get_s3_client(region_name: str):
    return boto3.client("s3", region_name=region_name)

def get_gcs_client():
    return storage.Client()

def get_translate_client():
    return translate.Client()

def get_vertex_ai_model(project_id: str, location: str, model_name: str):
    aiplatform.init(project=project_id, location=location)
    return aiplatform.GenerativeModel(model_name)

def get_vertex_ai_text_client(project_id: str, location: str):
    aiplatform.init(project=project_id, location=location)
    # This is a placeholder; actual safety checking might involve a specific pre-trained model or custom endpoint.
    # For demonstration, we'll use a generic text model if a specific safety model isn't readily available via SDK.
    return aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
