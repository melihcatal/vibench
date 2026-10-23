import boto3

bedrock = boto3.client('bedrock-runtime')

def check_corpus_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
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
    return result['results'][0]['outputText']