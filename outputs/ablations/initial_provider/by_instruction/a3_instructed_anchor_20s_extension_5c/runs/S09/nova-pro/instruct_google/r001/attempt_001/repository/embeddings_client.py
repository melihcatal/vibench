from google.cloud import aiplatform

def get_client():
    return aiplatform.gapic.PredictionServiceClient()

def get_model_name():
    return 'projects/1234567890/locations/us-central1/models/text-embedding-v1'