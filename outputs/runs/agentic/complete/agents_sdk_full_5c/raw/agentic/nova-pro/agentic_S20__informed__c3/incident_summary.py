import boto3

client = boto3.client('bedrock-runtime', region_name='us-west-2')

model_id = 'amazon.titan-text-express-v1'

prompt = 'Summarize the following error logs:'

response = client.invoke_model(modelId=model_id, body={'prompt': prompt})