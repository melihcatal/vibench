import os
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class LoggingConfig:
    """Configuration for logging service connections."""

    provider: str
    project_id: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    region: Optional[str] = None
    endpoint: Optional[str] = None
    workspace_id: Optional[str] = None
    environment: str = "development"


def load_logging_config() -> LoggingConfig:
    """
    Load logging configuration from environment variables.
    Supports multiple cloud providers.
    """
    provider = os.environ.get("LOGGING_PROVIDER", "google")

    if provider == "google":
        return LoggingConfig(
            provider="google",
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            environment=os.environ.get("ENVIRONMENT", "development"),
        )
    elif provider == "aws":
        return LoggingConfig(
            provider="aws",
            api_key=os.environ.get("AWS_ACCESS_KEY_ID"),
            api_secret=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region=os.environ.get("AWS_REGION", "us-east-1"),
            environment=os.environ.get("ENVIRONMENT", "development"),
        )
    elif provider == "azure":
        return LoggingConfig(
            provider="azure",
            workspace_id=os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID"),
            environment=os.environ.get("ENVIRONMENT", "development"),
        )
    elif provider == "datadog":
        return LoggingConfig(
            provider="datadog",
            api_key=os.environ.get("DD_API_KEY"),
            api_secret=os.environ.get("DD_APP_KEY"),
            endpoint=os.environ.get("DD_SITE", "datadoghq.com"),
            environment=os.environ.get("ENVIRONMENT", "development"),
        )
    else:
        return LoggingConfig(
            provider="console", environment=os.environ.get("ENVIRONMENT", "development")
        )


def get_logging_client():
    """
    Get a logging client based on the configured provider.
    Returns a provider-specific client object.
    """
    config = load_logging_config()

    if config.provider == "google":
        try:
            from google.cloud import logging_v2

            client = logging_v2.Client(project=config.project_id)
            return client
        except ImportError:
            print(
                "Google Cloud Logging client not available. Install google-cloud-logging"
            )
            return None

    elif config.provider == "aws":
        try:
            import boto3
            from botocore.config import Config

            client = boto3.client(
                "logs",
                aws_access_key_id=config.api_key,
                aws_secret_access_key=config.api_secret,
                region_name=config.region,
                config=Config(retries={"max_attempts": 3}),
            )
            return client
        except ImportError:
            print("AWS boto3 client not available. Install boto3")
            return None

    elif config.provider == "azure":
        try:
            from azure.identity import DefaultAzureCredential
            from azure.monitor.query import LogsQueryClient

            credential = DefaultAzureCredential()
            client = LogsQueryClient(credential)
            return client
        except ImportError:
            print(
                "Azure Monitor client not available. Install azure-monitor-query and azure-identity"
            )
            return None

    elif config.provider == "datadog":
        try:
            from datadog_api_client import ApiClient, Configuration
            from datadog_api_client.v2.api.logs_api import LogsApi

            api_config = Configuration()
            api_config.api_key["apiKeyAuth"] = config.api_key
            api_config.api_key["appKeyAuth"] = config.api_secret
            api_config.server_variables["site"] = config.endpoint

            api_client = ApiClient(api_config)
            client = LogsApi(api_client)
            return client
        except ImportError:
            print("Datadog API client not available. Install datadog-api-client")
            return None

    else:
        print(f"Using console logging for provider: {config.provider}")
        return None


def normalize_log_entry(entry: Dict[str, Any], provider: str) -> Dict[str, Any]:
    """
    Normalize log entry from different providers to a common format.
    """
    normalized = {
        "timestamp": "",
        "message": "",
        "service": "",
        "level": "INFO",
        "raw": entry,
    }

    if provider == "google":
        if "timestamp" in entry:
            normalized["timestamp"] = entry["timestamp"]
        if "json_payload" in entry and "message" in entry["json_payload"]:
            normalized["message"] = entry["json_payload"]["message"]
        if "labels" in entry and "service" in entry["labels"]:
            normalized["service"] = entry["labels"]["service"]
        if "severity" in entry:
            normalized["level"] = entry["severity"]

    elif provider == "aws":
        if "@timestamp" in entry:
            normalized["timestamp"] = entry["@timestamp"]
        if "@message" in entry:
            normalized["message"] = entry["@message"]
        if "logGroup" in entry:
            normalized["service"] = entry["logGroup"].split("/")[-1]

    elif provider == "azure":
        if "TimeGenerated" in entry:
            normalized["timestamp"] = entry["TimeGenerated"]
        if "Message" in entry:
            normalized["message"] = entry["Message"]
        if "AppRoleName" in entry:
            normalized["service"] = entry["AppRoleName"]
        if "SeverityLevel" in entry:
            normalized["level"] = entry["SeverityLevel"]

    elif provider == "datadog":
        if "timestamp" in entry:
            normalized["timestamp"] = entry["timestamp"]
        if "message" in entry:
            normalized["message"] = entry["message"]
        if "service" in entry:
            normalized["service"] = entry["service"]
        if "status" in entry:
            normalized["level"] = entry["status"].upper()

    return normalized


def validate_log_level(level: str) -> str:
    """
    Validate and normalize log level.
    """
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    level_upper = level.upper()

    if level_upper in valid_levels:
        return level_upper

    for valid_level in valid_levels:
        if level_upper.startswith(valid_level[:3]):
            return valid_level

    return "INFO"
