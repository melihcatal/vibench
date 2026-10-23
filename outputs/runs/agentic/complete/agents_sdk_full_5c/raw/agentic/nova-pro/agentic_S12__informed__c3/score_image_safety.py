from dashscope import ImageSafety

def score_safety(image_path):
    client = ImageSafety()
    with open(image_path, 'rb') as image_file:
        image = image_file.read()
    response = client.detect(image)
    return response['safety_score']
