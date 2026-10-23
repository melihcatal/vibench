import boto3

def check_corpus_text(text):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-lite-v1',
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    result = json.loads(response['body'].read())
    return result['results'][0]['outputText'] if result['results'] else None

if __name__ == '__main__':\n    text = 'Sample corpus text to check.'
    checked_text = check_corpus_text(text)
    print(checked_text)