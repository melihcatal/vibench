import boto3

def stream_completion(prompt, model_id='amazon.titan-text-express-v1'):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id=model_id,
        body={
            'prompt': prompt,
            'maxTokens': 150,
            'temperature': 0.5
        }
    )
    for event in response['body']['stream']:
        yield event['token']