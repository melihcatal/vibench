import boto3

def summarize_text(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.bedrock.summarization',
        body={
            'text': text
        }
    )
    summary = response['summary']
    return summary
