import os
import boto3

# Set up the Bedrock client
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def summarize_onboarding_state(text):
    try:
        response = bedrock_client.invoke_model(
            ModelId="amazon.titan-text-express-v1", Body=text
        )
        return response
    except Exception as e:
        print(e)
