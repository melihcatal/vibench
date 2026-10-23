import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def extract_json(text):
    model_id = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    content_type = 'application/json'
    body = {'inputText': text}
    response = bedrock_runtime.invoke_model(modelId=model_id, accept=accept, contentType=content_type, body=json.dumps(body))
    result = json.loads(response['body'].read())
    return result['json']