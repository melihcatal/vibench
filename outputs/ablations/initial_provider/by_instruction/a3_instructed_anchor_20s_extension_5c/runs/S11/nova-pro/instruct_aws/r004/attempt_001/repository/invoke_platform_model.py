import boto3

def invoke_platform_model(model_id, input_text):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': input_text
        }
    )
    return response