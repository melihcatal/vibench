from vision_client import get_vision_client

def detect_image_text(image_path):
    client = get_vision_client()
    response = client.image_analysis(image_path, features=['text'])
    return response['text']