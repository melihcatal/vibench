import boto3

def check_unsafe_content(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 4096,
                'stopSequences': [],
                'temperature': 0,
                'topP': 0.9
            }
        }
    )
    result = json.loads(response['body'].read())
    output_text = result['results'][0]['outputText']
    safety_check = result['results'][0]['safetyCheck']
    if safety_check['status'] == 'unsafe':
        print('Unsafe content detected:', output_text)
    else:
        print('Content is safe:', output_text)

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for unsafe content.'
    check_unsafe_content(sample_text)