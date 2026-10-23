import os
import dashscope

# DashScope client configured with API key from environment
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def score_image_safety(image_path: str) -> bool:
    """Check an image for unsafe or policy-sensitive visual content using DashScope.

    Returns True if the image is safe, False otherwise.
    """
    response = dashscope.vision.analyze_safety(image=image_path)
    # Assuming the response contains a 'safe' boolean flag
    return response.get('safe', False)
