import os
import dashscope

# DashScope client configured with API key from environment
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def detect_image_text(image_path: str) -> list:
    """Detect text appearing inside an image using DashScope.

    Returns a list of detected text strings.
    """
    response = dashscope.vision.detect_text(image=image_path)
    texts = [result['text'] for result in response.get('text_results', [])]
    return texts
