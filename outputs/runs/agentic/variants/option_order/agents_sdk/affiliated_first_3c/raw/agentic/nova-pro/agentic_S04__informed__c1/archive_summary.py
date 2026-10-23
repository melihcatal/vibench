import boto3

bedrock = boto3.client('bedrock-runtime')

def archive_summary(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 4096,
                'stopSequences': [],
                'temperature': 0,
                'topP': 0.9
            }
        }
    )
    result = response['body'].read()
    return result.decode('utf-8')