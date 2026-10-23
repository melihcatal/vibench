import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def stream_completion(text):
    model_id = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    content_type = 'application/json'
    body = {'inputText': text}
    response = bedrock_runtime.invoke_model_with_response_stream(modelId=model_id, accept=accept, contentType=content_type, body=json.dumps(body))
    for event in response['body']['events']:
        if 'chunk' in event:
            yield event['chunk']