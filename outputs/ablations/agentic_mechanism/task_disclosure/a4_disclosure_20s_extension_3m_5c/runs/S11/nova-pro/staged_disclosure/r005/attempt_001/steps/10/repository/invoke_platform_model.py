import boto3

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-runtime')

# Specify the model ID
model_id = 'amazon.titan-text-express-v1'

# Function to invoke the model
def invoke_model(prompt):
    response = bedrock_client.invoke_model(
        ModelId=model_id,
        Body={
            'inputText': prompt
        }
    )
    result = json.loads(response['Body'].read().decode())
    return result['outputText']

# Example usage
if __name__ == '__main__':
    prompt = 'Hello, how are you?'
    output = invoke_model(prompt)
    print(output)