import os
from bedrock import BedrockClient

# Configuration
AWS_REGION = 'us-west-2'
MODEL_FAMILY = 'amazon.titan-text-express-v1'

# Client Initialization
bedrock_client = BedrockClient(region_name=AWS_REGION)

# Helper Functions
def get_model_family():
    return MODEL_FAMILY

def infer_with_model(prompt):
    response = bedrock_client.invoke_model(
        model_id=MODEL_FAMILY,
        body={"prompt": prompt, "max_tokens": 150}
    )
    return response['body']['generated_text']