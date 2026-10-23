import boto3

def describe_image(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    labels = [label['Name'] for label in response['Labels'] if label['Confidence'] > 70]
    return ' '.join(labels)

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    print(describe_image(image_path))