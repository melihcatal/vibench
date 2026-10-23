from.vision_client import VisionClient

def describe_image(image_url, endpoint, key):
    client = VisionClient(endpoint, key)
    result = client.analyze_image(image_url, [VisualFeatures.CAPTION])
    return result.caption