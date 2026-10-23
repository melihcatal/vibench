import os
from typing import Dict
from dotenv import load_dotenv
from bedrock_client import BedrockRuntimeClient
from bedrock_client.types import ChatMessage, SendMessageRequest

load_dotenv()
BEDROCK_ENDPOINT = os.getenv('BEDROCK_ENDPOINT')
BEDROCK_API_KEY = os.getenv('BEDROCK_API_KEY')
MODEL_ID = 'amazon.titan-text-express-v1'

def generate_response(prompt: str) -> str:
    """Generate a response using Amazon Bedrock's Titan chat model."""
    client = BedrockRuntimeClient(endpoint=BEDROCK_ENDPOINT, api_key=BEDROCK_API_KEY)
    messages = [ChatMessage(role='user', content=[{'text': prompt}])]
    request = SendMessageRequest(messages=messages, model_id=MODEL_ID)
    response = client.send_message(request)
    return response.choices[0].message.content[0]['text']

# Example usage (illustrative)
if __name__ == '__main__':
    print(generate_response('Hello, how are you?'))

# End of login_audit_store.py