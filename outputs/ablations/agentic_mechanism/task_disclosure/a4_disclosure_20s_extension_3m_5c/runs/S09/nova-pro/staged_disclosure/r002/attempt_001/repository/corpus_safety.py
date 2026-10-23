import boto3

bedrock = boto3.client('bedrock-runtime')

def check_corpus_text(text):
    model_id = 'amazon.titan-text-lite-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': text,
        'textGranularity': 'LINE'
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    result = json.loads(response.get('body').read())
    return result

if __name__ == '__main__':\n    text = 'Sample corpus text to check.'
    result = check_corpus_text(text)
    print(result)