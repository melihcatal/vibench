import os
from google.cloud import aiplatform
from vision_client import get_vertex_ai_multimodal_model
from vision_models import ImageData, ImageDescriptionResult
from vertexai.preview.generative_models import Image as VertexImage, Part, GenerativeModel, HarmCategory, HarmBlockThreshold
import base64

def describe_image(image_data: ImageData, prompt: str = "Describe this image in detail.") -> ImageDescriptionResult:
    """
    Generates a short visual description for an image using Google Cloud Vertex AI
    with the Gemini Pro Vision model.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Specific location for Gemini Pro Vision
    model_name = "gemini-pro-vision"

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    model = get_vertex_ai_multimodal_model(project_id, location, model_name)

    image_part = None
    if image_data.content:
        image_bytes = base64.b64decode(image_data.content)
        image_part = VertexImage.from_bytes(image_bytes)
    elif image_data.gcs_uri:
        image_part = VertexImage.from_uri(image_data.gcs_uri)
    else:
        raise ValueError("No image content or GCS URI provided.")

    contents = [image_part, prompt]

    response = model.generate_content(
        contents,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    return ImageDescriptionResult(description=response.text)
