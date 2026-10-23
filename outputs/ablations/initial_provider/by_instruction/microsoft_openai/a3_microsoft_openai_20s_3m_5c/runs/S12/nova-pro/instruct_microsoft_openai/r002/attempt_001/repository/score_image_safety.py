from.vision_client import VisionClient

def score_image_safety(image_path):
    client = VisionClient().get_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data)
        return result.safety