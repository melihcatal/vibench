import boto3

def summarize_text(text):
    bedrock_client = boto3.client('bedrock', region_name='us-east-1')
    model_id = 'amazon.bedrock.summarization-001'
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body={
            'text': text
        }
    )
    return response['summary']