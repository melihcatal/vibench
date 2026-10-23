import os
import dashscope

# DashScope client configured with API key from environment
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def describe_image(image_path: str) -> str:
    """Generate a concise visual description for a static image using DashScope Qwen-VL.

    Returns a short natural-language description.
    """
    response = dashscope.vision.describe_image(image=image_path, model='qwen-vl')
    # Extract the generated description; field name may vary by provider
    description = response.get('description', '')
    return description
