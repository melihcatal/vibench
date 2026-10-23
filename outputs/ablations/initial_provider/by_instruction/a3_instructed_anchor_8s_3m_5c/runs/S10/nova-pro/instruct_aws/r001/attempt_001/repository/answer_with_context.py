import boto3
import json

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-text-express-v1'
    response = client.invoke_model(
        model_id=model_id,
        body={
            'inputText': f'Answer the following question using the provided context: {question}. Context: {context}',
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    result = json.loads(response['body'].read())
    return result['results'][0]['outputText']