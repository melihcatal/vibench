import os
from google.cloud import aiplatform

def get_model_client(project_id, location):
    aiplatform.init(project=project_id, location=location)
    return aiplatform