import os
from google.cloud import aiplatform

def get_client():
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    return aiplatform.PredictionServiceClient()