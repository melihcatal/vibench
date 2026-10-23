import os
import boto3

bedrock_client = boto3.client('bedrock-runtime')

def summarize_audit_events(events):
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': str(events),
            'textGenerationConfig': {
                'maxTokenCount': 4096,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    print(response['body'].read().decode('utf-8'))

if __name__ == '__main__':
    summarize_audit_events(['event1', 'event2'])