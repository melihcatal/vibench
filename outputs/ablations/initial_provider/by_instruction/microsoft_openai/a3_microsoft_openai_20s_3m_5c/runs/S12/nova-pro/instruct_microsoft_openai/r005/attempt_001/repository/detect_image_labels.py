from.vision_client import VisionClient

def detect_image_labels(image_url, endpoint, key):
    client = VisionClient(endpoint, key)
    result = client.analyze_image(image_url, [VisualFeatures.OBJECTS])
    return [obj.name for obj in result.objects]