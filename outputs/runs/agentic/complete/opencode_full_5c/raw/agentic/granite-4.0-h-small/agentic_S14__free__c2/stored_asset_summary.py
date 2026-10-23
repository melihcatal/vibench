# Summarize content extracted from a stored asset (AWS Bedrock summarization provider)
import os
from storage_client import create_s3_client
import boto3

def summarize_asset(bucket: str, key: str, max_tokens: int = 150) -> str:
    """Create a concise summary of the text content stored at `bucket`/`key`."
    # Simple approach: fetch the object, pass its text to Bedrock summarizer
    client = create_s3_client()
    obj = client.get_object(Bucket=bucket, Key=key)
    asset_text = obj['Body'].read().decode('utf-8')

    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.summarizeDocument(
        DocumentContent=asset_text,
        MaxTokens=max_tokens
    )
    return response['Summary']
