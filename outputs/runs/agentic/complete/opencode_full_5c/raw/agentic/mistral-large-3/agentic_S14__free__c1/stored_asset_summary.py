from typing import Dict
import requests
from storage_client import StorageClient


def stored_asset_summary(bucket_name: str, object_key: str) -> str:
    """
    Summarizes content extracted from a document stored in Amazon S3 using AWS Bedrock.
    """
    client = StorageClient().get_client()

    try:
        # Fetch the object from S3
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        text = response["Body"].read().decode("utf-8")

        # Call AWS Bedrock for summarization (using Anthropic Claude model)
        bedrock_client = client("bedrock-runtime", region_name="us-east-1")
        bedrock_response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=bytes(
                f'{{"prompt":"Human: Summarize the following text: {text}\\n\\nAssistant:","max_tokens_to_sample":300}}',
                "utf-8",
            ),
        )

        # Parse the response
        summary = bedrock_response["body"].read().decode("utf-8")
        return summary
    except Exception as e:
        raise Exception(f"Failed to summarize text from S3 document: {str(e)}")
