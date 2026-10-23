import os
from google.cloud import aiplatform

def init_client(project_id, location):
    aiplatform.init(project=project_id, location=location)

def get_endpoint(endpoint_id):
    return aiplatform.Endpoint(endpoint_id)

def get_model(model_id):
    return aiplatform.Model(model_id)