import boto3

def static_image_request(image_data):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.titan-image-generator-v1',
        body=image_data
    )
    return response

def static_image_response(response):
    return response['output']['generated_image']

def visual_understanding_request(image_data):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.titan-image-understanding-v1',
        body=image_data
    )
    return response

def visual_understanding_response(response):
    return response['output']['detected_objects']

def normalize_image(image_data):
    # Normalization logic here
    return normalized_image_data