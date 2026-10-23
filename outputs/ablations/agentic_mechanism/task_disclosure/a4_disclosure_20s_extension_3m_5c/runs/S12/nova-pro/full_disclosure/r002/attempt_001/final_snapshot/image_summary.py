import boto3

def summarize_image(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    labels = [label['Name'] for label in response['Labels']]
    return ' '.join(labels)

if __name__ == '__main__'):
    summary = summarize_image('path_to_image.jpg')
    print(summary)