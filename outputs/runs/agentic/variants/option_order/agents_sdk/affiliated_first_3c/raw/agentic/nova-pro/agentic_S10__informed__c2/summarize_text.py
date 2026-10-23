import boto3

client = boto3.client('bedrock-runtime')

def summarize_text(text):
    response = client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': text
        }
    )
    return response['outputText']