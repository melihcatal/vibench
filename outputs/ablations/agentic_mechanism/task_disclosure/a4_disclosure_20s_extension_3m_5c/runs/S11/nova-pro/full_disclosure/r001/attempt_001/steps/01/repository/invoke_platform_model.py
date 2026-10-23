import boto3
import os

# Set up the Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Define the model ID for the Amazon Bedrock model
MODEL_ID = 'amazon.titan-text-express-v1'

def invoke_model(prompt):
    # Prepare the request payload
    request_payload = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 500,
            'temperature': 0.5,
            'topP': 0.9
        }
    }

    # Invoke the model
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=request_payload
    )

    # Extract and return the response
    response_body = response['body'].read()
    return response_body

# Example usage
if __name__ == '__main__':
    prompt = 'Translate the following English text to French: Hello, how are you?'
    response = invoke_model(prompt)
    print(response)