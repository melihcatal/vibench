import vision_client

def describe_image(image_path):
    client = vision_client.get_vision_client()
    response = client.image_analysis.analyze(image_path, visual_features=['caption'])
    return response.caption