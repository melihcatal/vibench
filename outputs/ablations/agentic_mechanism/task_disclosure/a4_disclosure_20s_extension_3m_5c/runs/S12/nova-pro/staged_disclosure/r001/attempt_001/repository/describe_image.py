import boto3

def describe_image(image_path):
    client = boto3.client('bedrock-runtime')
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    response = client.invoke_model(
        model_id='amazon.titan-image-generator-v1',
        body=image_bytes
    )
    result = response['body'].read()
    description = result.decode('utf-8')
    return description

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    print(describe_image(image_path))