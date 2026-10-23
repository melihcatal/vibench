import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.api.logs_api import LogsApi


DATADOG_DEFAULT_SITE = "datadoghq.com"
DATADOG_API_HOST = "api.datadoghq.com"


def get_datadog_configuration() -> Configuration:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY environment variables must be set")
    site = os.environ.get("DD_SITE", DATADOG_DEFAULT_SITE)
    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.server_variables = {"site": site}
    config.host = f"https://{DATADOG_API_HOST}"
    return config


def create_datadog_metrics_client() -> MetricsApi:
    config = get_datadog_configuration()
    api_client = ApiClient(config)
    return MetricsApi(api_client)


def create_datadog_logs_client() -> LogsApi:
    config = get_datadog_configuration()
    api_client = ApiClient(config)
    return LogsApi(api_client)


def build_metric_query_string(
    metric_name: str, dimensions: dict[str, str] | None = None
) -> str:
    parts = [metric_name]
    if dimensions:
        for key, value in sorted(dimensions.items()):
            parts.append(f"{key}:{value}")
    return "{" + " ".join(parts) + "}"


def parse_datadog_response(raw_response: dict) -> list[dict]:
    series_list = raw_response.get("series", [])
    return series_list


def validate_time_window(start_ts: int, end_ts: int) -> None:
    if start_ts >= end_ts:
        raise ValueError("start_time must be before end_time")
    if end_ts - start_ts > 86400 * 30:
        raise ValueError("time window cannot exceed 30 days")
