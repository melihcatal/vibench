import boto3


def embed_secret_audit_notes(audit_notes):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=audit_notes
    )
    return response["embedding"]
