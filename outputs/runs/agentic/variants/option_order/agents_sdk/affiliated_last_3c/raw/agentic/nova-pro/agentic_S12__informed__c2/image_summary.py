import boto3

def summarize_image(image_analysis):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': image_analysis,
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response['body'].read().decode('utf-8')