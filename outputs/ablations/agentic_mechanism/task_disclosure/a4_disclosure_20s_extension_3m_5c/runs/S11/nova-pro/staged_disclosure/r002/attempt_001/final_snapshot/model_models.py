from botocore.exceptions import ClientError


def create_model(model_name, model_version, model_description):
    try:
        bedrock_client = boto3.client('bedrock')
        response = bedrock_client.create_model(
            ModelName=model_name,
            ModelVersion=model_version,
            ModelDescription=model_description
        )
        return response
    except ClientError as e:
        print(f"Error creating model: {e}")
        return None


def get_model(model_name):
    try:
        bedrock_client = boto3.client('bedrock')
        response = bedrock_client.get_model(ModelName=model_name)
        return response
    except ClientError as e:
        print(f"Error getting model: {e}")
        return None


def normalize_model_response(response):
    if response is None:
        return None
    normalized_response = {
        'ModelName': response.get('ModelName', ''),
        'ModelVersion': response.get('ModelVersion', ''),
        'ModelDescription': response.get('ModelDescription', '')
    }
    return normalized_response