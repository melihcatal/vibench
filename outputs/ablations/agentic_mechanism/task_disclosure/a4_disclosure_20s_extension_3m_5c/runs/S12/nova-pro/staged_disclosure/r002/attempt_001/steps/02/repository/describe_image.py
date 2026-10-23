import boto3
import json

def describe_image(image_path):
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    response = bedrock.invoke_model(
        model_id='amazon.titan-image-generator-v1',
        body=json.dumps({
            'input_data': {
                'image': image_bytes
            }
        })
    )
    response_body = json.loads(response['body'].read())
    description = response_body['description']
    return description

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    print(describe_image(image_path))