import os
from google.cloud import aiplatform

def select_platform_resource():
    project = 'your-gcp-project'
    location = 'us-central1'
    model_name = 'your-model-name'
    model = aiplatform.Model(model_name=model_name, project=project, location=location)
    return model