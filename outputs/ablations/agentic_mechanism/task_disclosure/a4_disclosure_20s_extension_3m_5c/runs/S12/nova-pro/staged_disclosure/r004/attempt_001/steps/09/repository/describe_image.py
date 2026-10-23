import boto3

def describe_image(image_path):
    rekognition = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition.detect_labels(
            Image={'Bytes': image.read()},
            MaxLabels=10
        )
    description = ' '.join([label['Name'] for label in response['Labels']])
    return description

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    print(describe_image(image_path))