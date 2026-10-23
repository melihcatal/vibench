from.vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient().get_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data)
        return result.caption