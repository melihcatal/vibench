import boto3

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-runtime')

# Specify the model ID
model_id = 'amazon.titan-text-express-v1'

def invoke_model(prompt):
    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body={
                'inputText': prompt
            }
        )
        result = json.loads(response['body'].read())
        return result['outputText']
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == '__main__':
    prompt = 'Translate the following English text to French: Hello, how are you?'
    result = invoke_model(prompt)
    if result:
        print(result)