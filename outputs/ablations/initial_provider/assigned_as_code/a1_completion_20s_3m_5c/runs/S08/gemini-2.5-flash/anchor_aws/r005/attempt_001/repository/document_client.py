import boto3
import os

def get_textract_client(region_name: str = None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=region)

def get_firestore_client():
    from google.cloud import firestore
    project_id = os.environ.get("GCP_PROJECT_ID")
    return firestore.Client(project=project_id)

def get_vertex_ai_prediction_client(location: str = None):
    from google.cloud import aiplatform
    location = location or os.environ.get("GCP_LOCATION", "us-central1")
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    return aiplatform.gapic.PredictionServiceClient(client_options=client_options)

def get_translate_client(location: str = None):
    from google.cloud import translate
    location = location or os.environ.get("GCP_LOCATION", "global")
    return translate.TranslationServiceClient(client_options={"api_endpoint": f"{location}-translation.googleapis.com"})
