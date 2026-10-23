import boto3
import os

def get_dynamodb_client():
    """
    Provides a configured boto3 DynamoDB client.
    Reads AWS credentials and region from environment variables.
    """
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are typically loaded from env or AWS config
    # For local development, you might also point to a local DynamoDB instance
    # e.g., boto3.client('dynamodb', endpoint_url='http://localhost:8000')
    
    # Ensure AWS_REGION is set
    region_name = os.getenv("AWS_REGION", "us-east-1") 
    
    # You can also pass credentials explicitly if not using environment variables/profile
    # access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    # secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    # If using local DynamoDB for development:
    # endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")
    # if endpoint_url:
    #     return boto3.client('dynamodb', region_name=region_name, endpoint_url=endpoint_url)

    return boto3.client('dynamodb', region_name=region_name)

if __name__ == '__main__':
    # Example usage: check if client can be initialized
    # try:
    #     client = get_dynamodb_client()
    #     print("DynamoDB client initialized successfully.")
    #     # You could try listing tables as a basic check
    #     # response = client.list_tables()
    #     # print(f"Tables: {response.get('TableNames')}")
    # except Exception as e:
    #     print(f"Failed to initialize DynamoDB client: {e}")
    pass
