from vision_models import ImageDescription, VisualAnalysis
from vision_client import get_google_vision_client
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

def describe_image_content(image_uri: str) -> ImageDescription:
    """
    Generates a visual description for an image using Google's Gemini model.

    Args:
        image_uri: Publicly accessible URI of the image.

    Returns:
        An ImageDescription object.
    """
    client = get_google_vision_client()
    
    # Using gemini-1.5-flash as a concrete model example
    model = client.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = requests.get(image_uri, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        raise IOError(f"Failed to download image from {image_uri}: {e}")

    prompt = "Describe this image in one sentence for use as alternative text."

    api_response = model.generate_content([prompt, img])
    
    description_text = api_response.text.strip()
    
    return ImageDescription(
        description=description_text,
        provider="google_gemini_vision"
    )


def describe_image(analysis: VisualAnalysis) -> VisualAnalysis:
    """Generates a description and adds it to the analysis object."""
    if not analysis.source_uri:
        raise ValueError("Analysis object must have a source_uri")
        
    description = describe_image_content(image_uri=analysis.source_uri)
    analysis.description = description
    return analysis
