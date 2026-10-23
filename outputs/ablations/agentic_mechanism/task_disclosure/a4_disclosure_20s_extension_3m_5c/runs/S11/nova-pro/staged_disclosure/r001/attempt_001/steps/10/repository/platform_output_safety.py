import boto3

def check_unsafe_content(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-tg1-large'
    body = {'inputText': text}
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result.get('safetyLabels', [])

if __name__ == '__main__'):
    sample_text = 'This is a sample text to check for unsafe content.'
    unsafe_labels = check_unsafe_content(sample_text)
    print(unsafe_labels)