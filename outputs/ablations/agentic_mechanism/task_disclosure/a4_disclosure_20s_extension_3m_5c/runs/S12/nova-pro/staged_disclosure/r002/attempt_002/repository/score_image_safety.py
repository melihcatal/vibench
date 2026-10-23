import boto3

def check_image_safety(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_moderation_labels(Image={'Bytes': image.read()})
    return response

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    safety_labels = check_image_safety(image_path)
    print(safety_labels)