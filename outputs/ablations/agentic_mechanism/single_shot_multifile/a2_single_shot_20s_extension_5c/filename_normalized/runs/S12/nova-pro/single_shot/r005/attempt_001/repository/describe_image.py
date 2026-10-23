from vision_client import get_vision_client

def describe_image(image_path):
    client = get_vision_client()
    response = client.image_analysis(image_path, features=['caption'])
    return response['caption'][0]['text']