import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI


@dataclass
class ObservabilityConfig:
    endpoint: str
    api_version: str
    metric_namespace: str
    metric_name: str
    resource_id: Optional[str] = None
    client_request_id: Optional[str] = None


def load_observability_config(overrides: Optional[Dict[str, Any]] = None) -> ObservabilityConfig:
    data = dict(overrides or {})
    endpoint = data.get("endpoint") or os.environ["AZURE_OPENAI_ENDPOINT"]
    api_version = data.get("api_version") or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
    metric_namespace = data.get("metric_namespace") or os.environ.get("METRIC_NAMESPACE", "managed.metrics")
    metric_name = data.get("metric_name") or os.environ.get("METRIC_NAME", "requests")
    return ObservabilityConfig(
        endpoint=endpoint,
        api_version=api_version,
        metric_namespace=metric_namespace,
        metric_name=metric_name,
        resource_id=data.get("resource_id") or os.environ.get("METRIC_RESOURCE_ID"),
        client_request_id=data.get("client_request_id") or os.environ.get("AZURE_CLIENT_REQUEST_ID"),
    )


def create_observability_client(config: Optional[ObservabilityConfig] = None) -> AzureOpenAI:
    cfg = config or load_observability_config()
    credential = DefaultAzureCredential()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint,
        api_version=cfg.api_version,
        azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token,
    )
