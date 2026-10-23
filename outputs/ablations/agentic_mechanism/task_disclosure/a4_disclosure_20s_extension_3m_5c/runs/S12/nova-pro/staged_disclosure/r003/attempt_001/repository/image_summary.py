import boto3

def summarize_image(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    return response['Labels']

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    labels = summarize_image(image_path)
    print('Detected labels:')
    for label in labels:
        print(f"{label['Name']}: {label['Confidence']}")