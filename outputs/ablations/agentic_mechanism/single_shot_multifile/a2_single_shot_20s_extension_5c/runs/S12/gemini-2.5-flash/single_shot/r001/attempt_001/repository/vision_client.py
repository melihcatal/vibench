import os
import base64
from google.cloud import vision_v1
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel
from typing import Optional, Dict, Any, Union
from vision_models import ImageData


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision AI client."""
    return vision_v1.ImageAnnotatorClient()

def get_vertex_ai_text_model(
    project_id: str,
    location: str,
    model_name: str,
) -> aiplatform.models.TextGenerationModel:
    """Initializes and returns a Google Cloud Vertex AI text generation model."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform.models.TextGenerationModel.from_pretrained(model_name)

def get_vertex_ai_multimodal_model(
    project_id: str,
    location: str,
    model_name: str,
) -> GenerativeModel:
    """
    Initializes and returns a Google Cloud Vertex AI multimodal model (e.g., Gemini Pro Vision).
    """
    aiplatform.init(project=project_id, location=location)
    return GenerativeModel(model_name)


def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encodes image bytes to a base64 string."""
    return base64.b64encode(image_bytes).decode('utf-8')

def create_vision_image_object(image_data: ImageData) -> vision_v1.Image:
    """Creates a Google Cloud Vision Image object from ImageData."""
    image = vision_v1.Image()
    if image_data.content:
        image.content = base64.b64decode(image_data.content)
    elif image_data.gcs_uri:
        image.source.image_uri = image_data.gcs_uri
    return image
