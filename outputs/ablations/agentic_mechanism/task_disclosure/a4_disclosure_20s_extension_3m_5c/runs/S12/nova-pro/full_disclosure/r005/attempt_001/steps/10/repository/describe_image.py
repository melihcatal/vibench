import boto3

def describe_image(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition_client.detect_labels(
            Image={'Bytes': image.read()},
            MaxLabels=10
        )
        labels = [label['Name'] for label in response['Labels']]
        return ' '.join(labels)

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    description = describe_image(image_path)
    print(description)