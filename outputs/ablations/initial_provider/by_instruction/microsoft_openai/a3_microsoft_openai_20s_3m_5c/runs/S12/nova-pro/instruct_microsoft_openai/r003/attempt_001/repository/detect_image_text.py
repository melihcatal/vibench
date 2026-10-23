from.vision_client import get_vision_client

def detect_image_text(image_path):
    client = get_vision_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data, features=['read'])
        return result.read.text
