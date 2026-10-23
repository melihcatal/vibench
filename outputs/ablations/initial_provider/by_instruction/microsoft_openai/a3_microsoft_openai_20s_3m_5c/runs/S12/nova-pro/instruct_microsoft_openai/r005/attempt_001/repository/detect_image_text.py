from.vision_client import VisionClient

def detect_image_text(image_url, endpoint, key):
    client = VisionClient(endpoint, key)
    result = client.analyze_image(image_url, [VisualFeatures.TEXT])
    return result.text