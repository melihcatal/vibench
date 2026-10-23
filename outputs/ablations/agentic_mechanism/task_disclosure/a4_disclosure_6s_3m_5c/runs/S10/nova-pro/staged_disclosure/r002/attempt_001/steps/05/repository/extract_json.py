import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

model_id = 'amazon.titan-text-express-v1'

def extract_json(text):
    response = bedrock.invoke_model(
        model_id=model_id,
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'stopSequences': ['
']
            }
        }
    )
    result = response['body'].read()
    return result
