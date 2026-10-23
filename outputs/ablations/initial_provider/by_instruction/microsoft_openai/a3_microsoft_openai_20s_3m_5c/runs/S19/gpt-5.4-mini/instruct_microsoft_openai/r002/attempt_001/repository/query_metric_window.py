import os
from typing import Any, Dict

from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

from observability_client import load_config
from observability_models import MetricWindowRequest, normalize_request


def query_metric_window(metric_name: str, start_time: str, end_time: str, resource_id: str = None, dimensions: Dict[str, str] = None) -> Dict[str, Any]:
    config = load_config()
    request = normalize_request(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_id=resource_id, dimensions=dimensions))
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")
    client = AzureOpenAI(
        api_key=config.azure_openai_api_key or token.token,
        azure_endpoint=config.azure_openai_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_version=config.azure_openai_api_version,
    )
    response = client.responses.create(
        model=config.azure_openai_deployment or "gpt-5.4-mini",
        input=[{"role": "user", "content": f"Query metric window: {request}"}],
    )
    return {"request": request, "provider": "Microsoft Azure OpenAI", "response": response.model_dump()}
