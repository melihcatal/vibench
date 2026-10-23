import boto3
import json

# Initialize a session using Amazon Bedrock
session = boto3.Session()
bedrock = session.client(
    service_name='bedrock',
    region_name='us-west-2'
)

# Define the model ID for the hosted LLM
model_id = 'amazon.bedrock.model.v1'

def stream_completion(prompt):
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({'prompt': prompt})
    )
    response_body = json.loads(response['body'].read())
    for token in response_body['completion']:
        yield token

# Example usage
for token in stream_completion('Once upon a time'):
    print(token)