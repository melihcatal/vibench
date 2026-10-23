import base64
from google.cloud.aiplatform_v1.types.content import Part, Content
from google.generative_models import GenerativeModel

from vision_client import get_google_vertex_ai_client
from vision_models import ImageDescription

def describe_image_content(image_bytes: bytes, prompt: str) -> ImageDescription:
    """
    Generates a description for an image using Google Gemini.

    Args:
        image_bytes: The byte content of the image.
        prompt: The prompt to guide the description generation.

    Returns:
        An ImageDescription object.
    """
    get_google_vertex_ai_client() # Initializes the client

    model = GenerativeModel("gemini-1.5-flash-001")
    
    image_part = Part(
        inline_data=base64.b64encode(image_bytes),
        mime_type="image/jpeg"
    )
    prompt_part = Part(text=prompt)

    generation_content = [image_part, prompt_part]
    
    response = model.generate_content(generation_content)

    return ImageDescription(text=response.text)
