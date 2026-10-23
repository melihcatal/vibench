import boto3
from botocore.exceptions import ClientError


def crypto_audit_embedding(audit_note):
    client = boto3.client("bedrock-runtime")
    try:
        response = client.invoke_model(
            ModelId="amazon.titan-embed-text-v1", Body=audit_note
        )
        return response["Embedding"]
    except ClientError as e:
        print(e)
        return None
