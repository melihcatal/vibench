from.vision_client import get_vision_client

def score_image_safety(image_path):
    client = get_vision_client()
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data, features=['adult'])
        return result.adult.is_adult_content
