from.vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient().get_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data)
        return result.objects