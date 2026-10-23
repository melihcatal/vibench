import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from google.cloud.aiplatform_v1beta1.types import ModelService

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

def initialize_vertex_ai():
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_generative_model(model_id: str) -> GenerativeModel:
    initialize_vertex_ai()
    # The GenerativeModel class from vertexai.preview.generative_models
    # implicitly uses the initialized Vertex AI project and location.
    return GenerativeModel(model_id)

def get_aiplatform_model_service_client():
    # This is an example of getting a more general AI Platform client
    # that could be used for listing models or other administrative tasks.
    # It's less for direct inference but useful for managing resources.
    return ModelService.ModelServiceClient(client_options={
        "api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"
    })