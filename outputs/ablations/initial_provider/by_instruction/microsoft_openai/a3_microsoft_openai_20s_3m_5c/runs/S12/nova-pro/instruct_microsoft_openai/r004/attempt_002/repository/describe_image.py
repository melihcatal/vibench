from.vision_client import get_vision_client

def describe_image(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_data:
        result = client.analyze(image_data, visual_features=[VisualFeatures.CAPTION])
        return result.caption.value