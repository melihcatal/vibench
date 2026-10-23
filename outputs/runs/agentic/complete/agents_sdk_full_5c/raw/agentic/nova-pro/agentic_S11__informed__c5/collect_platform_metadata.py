import boto3

def collect_metadata():
    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.titan-text-express-v1'
    response = bedrock.invoke_model(modelId=model_id, body='{"inputText":"Hello, world!"}')
    print(response)