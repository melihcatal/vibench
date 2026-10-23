import boto3

def summarize_text(text):
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-text-express-v1'
    payload = {
        'inputText': text,
        'textSize': {'maxToken': 512}
    }
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=payload
    )
    result = json.loads(response['body'].read())
    return result['outputText']

if __name__ == '__main__':
    text_to_summarize = 'Long text to be summarized goes here.'
    summary = summarize_text(text_to_summarize)
    print(summary)