import os
from google.cloud import aiplatform

def init_aiplatform():
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

def get_prediction_service_client():
    return aiplatform.PredictionServiceClient()