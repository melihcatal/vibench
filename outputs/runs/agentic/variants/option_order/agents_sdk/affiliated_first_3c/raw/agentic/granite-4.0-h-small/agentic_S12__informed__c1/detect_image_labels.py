import os
import dashscope

# Configure DashScope client with API key from environment
# DASHSCOPE_API_KEY must be set in the environment before running
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def detect_image_labels(image_path: str) -> list:
    """Detect objects/labels in a static image using Alibaba DashScope Qwen-VL model.

    Returns a list of detected label strings.
    """
    response = dashscope.vision.analyze_image(
        image=image_path,
        model='qwen-vl'
    )
    # The provider returns predictions in a provider-specific format.
    # Assuming each prediction has a 'label' field containing the detected label.
    labels = [result['label'] for result in response.get('predictions', [])]
    return labels
