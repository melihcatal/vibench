import os
import boto3

def select_bedrock_model(model_name: str) -> str:
    """
    Resolves a provider-specific model resource for AWS Bedrock.
    """
    # In a real application, you might validate the model_name against available models
    # or fetch specific ARNs/identifiers based on configuration or region.
    # For this example, we'll assume the model_name is directly usable.
    return f"arn:aws:bedrock:us-east-1::foundation-model/{model_name}"

def get_bedrock_client():
    """
    Returns an initialized AWS Bedrock client.
    """
    # AWS_REGION_NAME can be set as an environment variable or configured in ~/.aws/config
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    
    # The client will use credentials configured in environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or ~/.aws/credentials
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name
    )
    return client

if __name__ == "__main__":
    # Example usage:
    selected_model_arn = select_bedrock_model("anthropic.claude-v2")
    print(f"Selected Bedrock model ARN: {selected_model_arn}")

    try:
        bedrock_client = get_bedrock_client()
        # You can now use bedrock_client to invoke models, e.g.:
        # response = bedrock_client.invoke_model(
        #     modelId=selected_model_arn,
        #     contentType="application/json",
        #     accept="application/json",
        #     body=json.dumps({"prompt": "Hello", "max_tokens_to_sample": 100})
        # )
        print("Bedrock client initialized successfully (requires AWS credentials and region config).")
    except Exception as e:
        print(f"Failed to initialize Bedrock client: {e}")
