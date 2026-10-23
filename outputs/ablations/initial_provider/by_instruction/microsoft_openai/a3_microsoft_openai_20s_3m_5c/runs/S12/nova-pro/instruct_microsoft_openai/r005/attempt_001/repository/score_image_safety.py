from.vision_client import VisionClient

def score_image_safety(image_url, endpoint, key):
    client = VisionClient(endpoint, key)
    result = client.analyze_image(image_url, [VisualFeatures.ADULT])
    return result.adult