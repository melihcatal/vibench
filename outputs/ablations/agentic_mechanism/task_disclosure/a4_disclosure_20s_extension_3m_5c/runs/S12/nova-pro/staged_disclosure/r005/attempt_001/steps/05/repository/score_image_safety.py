import boto3

def check_image_safety(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition_client.detect_moderation_labels(
            Image={'Bytes': image.read()}
        )
        moderation_labels = response['ModerationLabels']
        for label in moderation_labels:
            print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")
        return moderation_labels

if __name__ == '__main__':
    image_path = 'path_to_image.jpg'
    check_image_safety(image_path)