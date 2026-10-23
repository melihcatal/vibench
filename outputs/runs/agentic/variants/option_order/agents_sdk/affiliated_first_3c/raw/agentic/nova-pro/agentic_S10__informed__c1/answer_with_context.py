import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def answer_with_context(question, context):
    model_id = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    content_type = 'application/json'
    body = {'inputText': question, 'context': context}
    response = bedrock_runtime.invoke_model(modelId=model_id, accept=accept, contentType=content_type, body=json.dumps(body))
    result = json.loads(response['body'].read())
    return result['answer']