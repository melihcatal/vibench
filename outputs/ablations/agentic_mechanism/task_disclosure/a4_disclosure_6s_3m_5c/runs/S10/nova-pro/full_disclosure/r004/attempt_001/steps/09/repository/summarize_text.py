import boto3

def summarize_text(text):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(
        model_id='amazon.bedrock.summarization',
        body={
            'text': text
        }
    )
    return response['summary']