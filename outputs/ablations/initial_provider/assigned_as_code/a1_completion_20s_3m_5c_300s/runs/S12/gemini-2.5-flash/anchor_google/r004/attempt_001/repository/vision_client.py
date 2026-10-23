import os
from google.cloud import vision
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def get_vision_client():
    return vision.ImageAnnotatorClient()

def get_gemini_pro_vision_model():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
    vertexai.init(project=project_id, location=location)
    return GenerativeModel("gemini-pro-vision")

def get_gemini_pro_model():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
    vertexai.init(project=project_id, location=location)
    return GenerativeModel("gemini-pro")
