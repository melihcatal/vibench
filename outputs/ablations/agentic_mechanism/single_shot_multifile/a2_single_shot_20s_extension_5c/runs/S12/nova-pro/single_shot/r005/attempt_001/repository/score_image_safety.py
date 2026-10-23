from vision_client import get_vision_client

def score_image_safety(image_path):
    client = get_vision_client()
    response = client.image_analysis(image_path, features=['adult'])
    return response['adult']