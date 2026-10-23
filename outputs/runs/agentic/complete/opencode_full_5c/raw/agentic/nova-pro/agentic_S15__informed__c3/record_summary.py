import boto3
from botocore.exceptions import NoCredentialsError


def record_summary(document):
    client = boto3.client("bedrock-runtime")
    try:
        response = client.invoke_model(
            model_id="amazon.titan-text-express-v1", body=document
        )
        return response["body"].read()
    except NoCredentialsError:
        print("No AWS credentials found")
        return None
