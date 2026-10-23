import boto3

def summarize_text(text):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.bedrock.summarization',
        body={
            'inputText': text
        }
    )
    return response['summary']