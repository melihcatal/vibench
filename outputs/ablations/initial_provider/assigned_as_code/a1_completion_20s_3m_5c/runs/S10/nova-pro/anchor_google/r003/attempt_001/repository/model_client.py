import os
from boto3 import client


def get_bedrock_client(region=None):
    region = region or os.environ.get('AWS_REGION')
    return client('bedrock-runtime', region_name=region)


def invoke_model(client, model_id, input_text, max_token_count=4096, temperature=0, top_p=0.9):
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': input_text,
            'textGenerationConfig': {
                'maxTokenCount': max_token_count,
                'temperature': temperature,
                'topP': top_p
            }
        }
    )
    return json.loads(response['body'].read())

