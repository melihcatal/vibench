import vision_client

def score_image_safety(image_path):
    client = vision_client.get_vision_client()
    response = client.image_analysis.analyze(image_path, visual_features=['adult'])
    return response.adult