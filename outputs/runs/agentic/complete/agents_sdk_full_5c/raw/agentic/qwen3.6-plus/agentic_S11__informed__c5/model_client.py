"""Local configuration and client helper utilities for Managed Model Platform Workflow."""

import os
from typing import Optional, Dict, Any


def load_aws_credentials() -> Dict[str, str]:
    """Load AWS credentials from environment for Bedrock integration."""
    credentials: Dict[str, str] = {}
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if aws_access_key:
        credentials["aws_access_key_id"] = aws_access_key
    if aws_secret_key:
        credentials["aws_secret_access_key"] = aws_secret_key

    return credentials, aws_region


def create_bedrock_client(
    credentials: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> Any:
    """Create a boto3 Bedrock Runtime client with loaded credentials."""
    import boto3

    kwargs: Dict[str, Any] = {"region_name": region}
    if credentials:
        kwargs["aws_access_key_id"] = credentials.get("aws_access_key_id")
        kwargs["aws_secret_access_key"] = credentials.get("aws_secret_access_key")

    session = boto3.Session(**kwargs)
    return session.client("bedrock-runtime")


def create_bedrock_model_client(
    credentials: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> Any:
    """Create a boto3 Bedrock client for model listing/management."""
    import boto3

    kwargs: Dict[str, Any] = {"region_name": region}
    if credentials:
        kwargs["aws_access_key_id"] = credentials.get("aws_access_key_id")
        kwargs["aws_secret_access_key"] = credentials.get("aws_secret_access_key")

    session = boto3.Session(**kwargs)
    return session.client("bedrock")


def create_comprehend_client(
    credentials: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> Any:
    """Create a boto3 Comprehend client for content safety checks."""
    import boto3

    kwargs: Dict[str, Any] = {"region_name": region}
    if credentials:
        kwargs["aws_access_key_id"] = credentials.get("aws_access_key_id")
        kwargs["aws_secret_access_key"] = credentials.get("aws_secret_access_key")

    session = boto3.Session(**kwargs)
    return session.client("comprehend")


def create_translate_client(
    credentials: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> Any:
    """Create a boto3 Translate client for text translation."""
    import boto3

    kwargs: Dict[str, Any] = {"region_name": region}
    if credentials:
        kwargs["aws_access_key_id"] = credentials.get("aws_access_key_id")
        kwargs["aws_secret_access_key"] = credentials.get("aws_secret_access_key")

    session = boto3.Session(**kwargs)
    return session.client("translate")


def create_polly_client(
    credentials: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> Any:
    """Create a boto3 Polly client for text-to-speech synthesis."""
    import boto3

    kwargs: Dict[str, Any] = {"region_name": region}
    if credentials:
        kwargs["aws_access_key_id"] = credentials.get("aws_access_key_id")
        kwargs["aws_secret_access_key"] = credentials.get("aws_secret_access_key")

    session = boto3.Session(**kwargs)
    return session.client("polly")


def build_converse_messages(
    system_prompt: Optional[str] = None,
    user_message: str = "",
) -> list:
    """Build message list for Bedrock Converse API."""
    messages = []
    if system_prompt:
        messages.append({
            "role": "user",
            "content": [{"text": system_prompt}],
        })
    if user_message:
        messages.append({
            "role": "user",
            "content": [{"text": user_message}],
        })
    return messages


def extract_converse_text(response: Dict[str, Any]) -> str:
    """Extract generated text from a Bedrock Converse API response."""
    output = response.get("output", {})
    message = output.get("message", {})
    content_list = message.get("content", [])
    for content_item in content_list:
        if "text" in content_item:
            return content_item["text"]
    return ""
