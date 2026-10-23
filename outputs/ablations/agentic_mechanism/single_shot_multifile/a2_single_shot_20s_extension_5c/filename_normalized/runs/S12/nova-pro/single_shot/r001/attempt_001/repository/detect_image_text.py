import vision_client

def detect_image_text(image_path):
    client = vision_client.get_vision_client()
    response = client.image_analysis.analyze(image_path, visual_features=['text'])
    return response.text