import boto3
import os


def summarize_aws_kms_key_usage(region_name: str = None) -> list[dict]:
    """Summarizes key usage for AWS KMS keys by listing them and their metadata."""
    if region_name is None:
        region_name = os.getenv("AWS_REGION", "us-east-1")

    client = boto3.client("kms", region_name=region_name)
    keys_summary = []
    paginator = client.get_paginator("list_keys")

    for page in paginator.paginate():
        for key in page.get("Keys", []):
            key_id = key["KeyId"]
            try:
                metadata = client.describe_key(KeyId=key_id)["KeyMetadata"]
                keys_summary.append(
                    {
                        "KeyId": metadata["KeyId"],
                        "Arn": metadata["Arn"],
                        "CreationDate": metadata["CreationDate"].isoformat(),
                        "KeyState": metadata["KeyState"],
                        "Origin": metadata["Origin"],
                        "KeyUsage": metadata["KeyUsage"],
                        "EncryptionAlgorithms": metadata.get(
                            "EncryptionAlgorithms", []
                        ),
                        "SigningAlgorithms": metadata.get("SigningAlgorithms", []),
                    }
                )
            except Exception as e:
                keys_summary.append({"KeyId": key_id, "Error": str(e)})
    return keys_summary
