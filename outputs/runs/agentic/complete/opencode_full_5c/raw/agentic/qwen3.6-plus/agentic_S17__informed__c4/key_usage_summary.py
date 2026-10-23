import os
import json
import boto3
from botocore.exceptions import ClientError
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse
from security_client import get_bedrock_client, get_kms_client


def summarize_key_usage(
    key_id=None, start_time=None, end_time=None, custom_summary_text=None
):
    request = KeyUsageSummaryRequest(
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        start_time=start_time,
        end_time=end_time,
        summary_text=custom_summary_text,
    )
    kms_client = get_kms_client()
    bedrock_client = get_bedrock_client()
    try:
        key_metadata = kms_client.describe_key(KeyId=request.key_id)
        key_info = key_metadata.get("KeyMetadata", {})
        key_state = key_info.get("KeyState", "Unknown")
        key_usage = key_info.get("KeyUsage", "ENCRYPT_DECRYPT")
        origin = key_info.get("Origin", "AWS_KMS")
        creation_date = key_info.get("CreationDate", "N/A")
        usage_context = ""
        if request.summary_text:
            usage_context = f"\n\nAdditional context:\n{request.summary_text}"
        prompt = f"""Summarize the following AWS KMS key usage information in a concise report:

Key ID: {request.key_id}
Key State: {key_state}
Key Usage: {key_usage}
Origin: {origin}
Creation Date: {creation_date}
Start Time: {request.start_time or "N/A"}
End Time: {request.end_time or "N/A"}
{usage_context}

Provide a brief summary of the key's purpose, current state, and any recommendations for key rotation or access management."""
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
        )
        response_body = json.loads(response["body"].read())
        summary_text = response_body["content"][0]["text"]
        return KeyUsageSummaryResponse(
            summary=summary_text,
            key_id=request.key_id,
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )
    except ClientError as e:
        raise RuntimeError(
            f"Key usage summary failed: {e.response['Error']['Message']}"
        ) from e
