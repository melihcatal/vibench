import boto3

AWS_REGION = 'us-west-2'
BEDROCK_SERVICE_NAME = 'bedrock-runtime'

def create_bedrock_client():
    return boto3.client(BEDROCK_SERVICE_NAME, region_name=AWS_REGION)

def create_embeddings(client, model_id, input_text):
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': input_text
        }
    )
    return response['embedding']