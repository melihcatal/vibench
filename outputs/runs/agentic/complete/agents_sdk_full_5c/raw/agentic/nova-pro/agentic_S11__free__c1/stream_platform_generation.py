import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_generation(prompt):
    model_id = 'amazon.titan-text-express-v1'
    body = {'inputText': prompt, 'textGenerationConfig': {'maxTokenCount': 512}}
    response = bedrock.invoke_model_with_response_stream(modelId=model_id, body=body)
    for event in response['body']['stream']:
        yield event