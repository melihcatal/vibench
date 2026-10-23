import vision_client

def detect_image_labels(image_path):
    client = vision_client.get_vision_client()
    response = client.image_analysis.analyze(image_path, visual_features=['objects'])
    return response.objects