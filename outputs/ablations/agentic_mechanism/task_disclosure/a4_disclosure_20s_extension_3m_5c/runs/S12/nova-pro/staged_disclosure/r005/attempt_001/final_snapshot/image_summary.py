import boto3

def summarize_image(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    return response['Labels']

if __name__ == '__main__':\n    image_path = 'path_to_image.jpg'\n    labels = summarize_image(image_path)\n    print(labels)