import boto3

bedrock = boto3.client('bedrock-runtime')

def invoke_model(prompt, model_id='amazon.titan-image-generator-v1'):
    body = {
        'taskType': 'TEXT_IMAGE_GENERATION',
        'textToGenerateImage': prompt,
        'imageGenerationConfig': {
            'numberOfImages': 1,
            'quality': 'standard',
            'cfgScale': 10,
            'height': 512,
            'width': 512
        }
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    return response_body

def normalize_response(response):
    images = response.get('images', [])
    normalized_images = []
    for image in images:
        normalized_image = {
            'image_data': image.get('imageData', ''),
            'seed': image.get('seed', 0)
        }
        normalized_images.append(normalized_image)
    return normalized_images