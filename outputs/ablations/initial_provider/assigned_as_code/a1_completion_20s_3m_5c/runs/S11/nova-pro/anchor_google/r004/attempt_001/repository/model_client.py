import os
from google.cloud import aiplatform

def model_client():
    project = 'your-gcp-project'
    location = 'us-central1'
    aiplatform.init(project=project, location=location)
    return aiplatform

client = model_client()