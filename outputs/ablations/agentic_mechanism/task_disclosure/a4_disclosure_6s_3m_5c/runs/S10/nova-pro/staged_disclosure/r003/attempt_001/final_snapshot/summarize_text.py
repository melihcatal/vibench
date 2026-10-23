import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def summarize_text(text):
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': text,
        'textGranularity': 'SUMMARY',
        'summarizationType': 'BASIC'
    }
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result.get('summary')

if __name__ == '__main__'):
    text = 'Long text to summarize...'
    summary = summarize_text(text)
    print(summary)