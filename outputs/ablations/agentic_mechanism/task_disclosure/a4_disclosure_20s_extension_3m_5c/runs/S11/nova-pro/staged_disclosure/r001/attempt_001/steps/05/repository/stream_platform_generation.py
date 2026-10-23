import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def generate_stream(prompt):
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': prompt,
            'textGenerationConfig': {
                'maxTokenCount': 500,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    response_body = response['body'].read()
    response_json = json.loads(response_body)
    results = response_json['results'][0]['outputText']
    yield results


if __name__ == '__main__':
    prompt = 'Write a short story about a robot learning to love.'
    for chunk in generate_stream(prompt):
        print(chunk, end='')