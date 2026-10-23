import boto3

bedrock = boto3.client('bedrock-runtime')

def invoke_model(prompt):
    model_id = 'amazon.titan-text-express-v1'
    body = {'inputText': prompt, 'textGenerationConfig': {'maxTokenCount': 512}}
    response = bedrock.invoke_model(modelId=model_id, body=body)
    return response