import os
from google.cloud import aiplatform

def select_model():
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    model_name = client.model_path('your-project-id', 'us-central1', 'your-model-id')
    return model_name