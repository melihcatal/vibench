import boto3

def check_image_safety(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    response = rekognition_client.detect_moderation_labels(Image={'Bytes': image_bytes})
    moderation_labels = response['ModerationLabels']
    return moderation_labels

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    safety_labels = check_image_safety(image_path)
    print(safety_labels)