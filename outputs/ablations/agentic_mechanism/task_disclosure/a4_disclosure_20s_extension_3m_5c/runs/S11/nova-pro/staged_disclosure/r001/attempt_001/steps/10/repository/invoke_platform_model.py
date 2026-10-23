import boto3

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Define the model ID
model_id = 'amazon.titan-text-express-v1'

# Function to invoke the model
def invoke_model(prompt):
    body = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    result = json.loads(response['body'].read())
    return result['results'][0]['outputText']

# Example usage
prompt = 'Generate a short story about a robot learning to love.'
output = invoke_model(prompt)
print(output)