import boto3

def check_image_safety(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_moderation_labels(Image={'Bytes': image.read()})
    for label in response['ModerationLabels']:
        if label['ParentName'] == '' and label['Confidence'] > 50:
            print(f"Unsafe content detected: {label['Name']} with confidence {label['Confidence']}")
    return response

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    check_image_safety(image_path)