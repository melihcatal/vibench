import boto3

def summarize_text(text):
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    response = bedrock.invoke_model(
        model_id='amazon.bedrock.summarization',
        body={
            'inputText': text
        }
    )
    return response['summary']