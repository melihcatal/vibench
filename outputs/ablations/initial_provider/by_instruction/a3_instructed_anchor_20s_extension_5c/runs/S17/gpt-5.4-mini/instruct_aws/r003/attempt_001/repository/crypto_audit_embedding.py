import boto3


def crypto_audit_embedding(note, region_name=None):
    bedrock = boto3.client("bedrock-runtime", region_name=region_name)
    return {"provider": "aws-bedrock", "embedding_model_id": "amazon.titan-embed-text-v1", "note": note}
