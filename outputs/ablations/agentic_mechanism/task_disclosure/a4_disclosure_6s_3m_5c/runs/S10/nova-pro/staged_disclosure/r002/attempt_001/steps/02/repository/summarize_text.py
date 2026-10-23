import boto3

def summarize_text(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result.get('results')[0].get('outputText')

if __name__ == '__main__'):
    text = 'Long text to summarize goes here.'
    summary = summarize_text(text)
    print(summary)