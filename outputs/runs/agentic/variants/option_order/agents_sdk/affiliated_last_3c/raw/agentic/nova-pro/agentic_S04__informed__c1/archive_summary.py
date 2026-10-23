import boto3

bedrock = boto3.client('bedrock-runtime')

def archive_summary(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response['body'].read().decode('utf-8')