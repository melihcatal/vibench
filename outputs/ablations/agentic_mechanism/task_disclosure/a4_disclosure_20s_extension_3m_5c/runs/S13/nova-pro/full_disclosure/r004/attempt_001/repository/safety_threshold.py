import boto3

BEDROCK_MODEL_ID = 'amazon.titan-text-express-v1'

def apply_thresholds(text):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id=BEDROCK_MODEL_ID,
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
    output_text = result['results'][0]['outputText']
    # Apply category thresholds based on the output_text
    # This is a placeholder for the actual threshold logic
    if 'unsafe' in output_text.lower():
        return False
    else:
        return True