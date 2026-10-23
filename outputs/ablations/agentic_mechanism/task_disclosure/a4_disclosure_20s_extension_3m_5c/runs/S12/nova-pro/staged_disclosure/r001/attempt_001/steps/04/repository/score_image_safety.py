import boto3

def score_image_safety(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_moderation_labels(Image={'Bytes': image.read()})
    moderation_labels = response['ModerationLabels']
    unsafe_labels = [label for label in moderation_labels if label['ParentName'] == '' and label['Confidence'] > 50]
    return unsafe_labels

if __name__ == '__main__':
    image_path = 'path_to_image.jpg'
    unsafe_labels = score_image_safety(image_path)
    print(unsafe_labels)