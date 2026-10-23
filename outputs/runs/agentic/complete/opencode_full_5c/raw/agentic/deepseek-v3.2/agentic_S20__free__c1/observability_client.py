import boto3
import os
from typing import Optional


class ObservabilityConfig:
    """Configuration for observability services."""

    def __init__(self):
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.cloudwatch_log_group = os.getenv(
            "CLOUDWATCH_LOG_GROUP", "/aws/lambda/my-application"
        )
        self.default_log_stream = os.getenv("DEFAULT_LOG_STREAM", "application-logs")

        # OpenAI configuration for later-step integrations
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Google Cloud Translation configuration
        self.google_project_id = os.getenv("GOOGLE_PROJECT_ID")

        # Hugging Face configuration for embeddings
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.huggingface_model = os.getenv(
            "HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )


def get_cloudwatch_client() -> boto3.client:
    """Get AWS CloudWatch Logs client for log ingestion."""
    config = ObservabilityConfig()
    return boto3.client("logs", region_name=config.aws_region)


def get_cloudwatch_logs_client() -> boto3.client:
    """Get AWS CloudWatch Logs Insights client for querying."""
    config = ObservabilityConfig()
    return boto3.client("logs", region_name=config.aws_region)


def get_openai_client():
    """Get OpenAI client for text processing."""
    try:
        import openai

        config = ObservabilityConfig()
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = openai.OpenAI(api_key=config.openai_api_key)
        return client
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )


def get_google_translate_client():
    """Get Google Cloud Translation client."""
    try:
        from google.cloud import translate_v2 as translate

        config = ObservabilityConfig()

        # For local development, you can set GOOGLE_APPLICATION_CREDENTIALS
        client = translate.Client()
        return client
    except ImportError:
        raise ImportError(
            "google-cloud-translate package not installed. Install with: pip install google-cloud-translate"
        )


def get_huggingface_client():
    """Get Hugging Face client for embeddings."""
    try:
        import requests

        config = ObservabilityConfig()
        if not config.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY environment variable not set")

        return {
            "api_key": config.huggingface_api_key,
            "model": config.huggingface_model,
            "api_url": f"https://api-inference.huggingface.co/pipeline/feature-extraction/{config.huggingface_model}",
        }
    except ImportError:
        raise ImportError(
            "requests package not installed. Install with: pip install requests"
        )


def normalize_log_event(event: dict) -> dict:
    """Normalize log event structure."""
    normalized = event.copy()

    # Ensure required fields
    if "timestamp" not in normalized:
        from datetime import datetime

        normalized["timestamp"] = int(datetime.now().timestamp() * 1000)

    if "level" not in normalized:
        normalized["level"] = "INFO"

    if "message" not in normalized:
        normalized["message"] = str(event)

    # Standardize field names
    field_mapping = {
        "severity": "level",
        "log_level": "level",
        "msg": "message",
        "text": "message",
        "time": "timestamp",
    }

    for old_key, new_key in field_mapping.items():
        if old_key in normalized and new_key not in normalized:
            normalized[new_key] = normalized.pop(old_key)

    return normalized


def parse_cloudwatch_response(response: dict) -> list:
    """Parse CloudWatch Logs query response."""
    results = []
    for item in response.get("results", []):
        parsed_item = {}
        for field in item:
            parsed_item[field["field"]] = field["value"]
        results.append(parsed_item)
    return results
