# observability_client.py
# LOCAL HELPER – Managed Metrics Monitoring

import os
from typing import Any

# Provider selection – uncomment the service you intend to use
# PROVIDER = "datadog"
# PROVIDER = "google"
# PROVIDER = "ibm"
# PROVIDER = "azure"
# PROVIDER = "aws"
# PROVIDER = "alibaba"

class ObservabilityClient:
    """Unified client wrapper for Managed Metrics Monitoring providers.

    Configuration is read from environment variables matching the chosen provider.
    """

    def __init__(self) -> None:
        self._client = self._init_client()

    def _init_client(self) -> Any:
        provider = os.getenv("MONITORING_PROVIDER", "datadog")
        if provider == "datadog":
            from datadog import initialize, api
            api_key = os.getenv("DD_API_KEY")
            app_key = os.getenv("DD_APP_KEY")
            if not api_key or not app_key:
                raise RuntimeError("DD_API_KEY and DD_APP_KEY must be set for Datadog")
            initialize(api_key=api_key, app_key=app_key)
            return api
        elif provider == "google":
            from google.cloud import monitoring_v3
            # Uses default credentials from GOOGLE_APPLICATION_CREDENTIALS
            client = monitoring_v3.MetricServiceClient()
            return client
        elif provider == "ibm":
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
            from ibm_monitoring import metrics as ibm_metrics
            api_key = os.getenv("IBM_CLOUD_API_KEY")
            instance_id = os.getenv("IBM_MONITORING_INSTANCE_ID")
            if not api_key or not instance_id:
                raise RuntimeError("IBM_CLOUD_API_KEY and IBM_MONITORING_INSTANCE_ID must be set for IBM Cloud Monitoring")
            authenticator = IAMAuthenticator(api_key)
            base_url = f"https://monitoring.{instance_id}.monitoring.cloud.ibm.com"
            return ibm_metrics.MetricsV1(authenticator=authenticator, url=base_url)
        elif provider == "azure":
            from azure.monitor.opentelemetry.exporter import AzureMonitorMetricsExporter
            from opentelemetry.sdk.metrics import MeterProvider
            account_url = os.getenv("AZURE_MONITOR_ACCOUNT_URL")
            access_key = os.getenv("AZURE_MONITOR_ACCESS_KEY")
            if not account_url or not access_key:
                raise RuntimeError("AZURE_MONITOR_ACCOUNT_URL and AZURE_MONITOR_ACCESS_KEY must be set for Azure Monitor")
            exporter = AzureMonitorMetricsExporter(namespace="custom/metrics", resource=None,
                                                   connection_string=f"InstrumentationKey={access_key}")
            meter = MeterProvider(metric_readers=[exporter]).get_meter("default")
            return exporter  # simple return of exporter for demo purposes
        elif provider == "aws":
            import boto3
            client = boto3.client(
                "cloudwatch",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
            return client
        elif provider == "alibaba":
            from alibabacloud_cms20190101.client import Client as CmsClient
            from alibabacloud_tea_util.model import Config
            access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
            access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
            if not access_key_id or not access_key_secret:
                raise RuntimeError("ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set for Alibaba CloudMonitor")
            config = Config(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
                endpoint="cms.cn-hangzhou.aliyuncs.com")
            client = CmsClient(config)
            return client
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def query_recent(self, metric_name: str, start: str, end: str, **kwargs) -> Any:
        """Delegate to provider-specific recent datapoint query.

        Args:
            metric_name: Metric identifier.
            start: ISO8601 start timestamp.
            end: ISO8601 end timestamp.
            **kwargs: Additional provider-specific parameters.
        """
        provider = os.getenv("MONITORING_PROVIDER", "datadog")
        if provider == "datadog":
            from datadog import api
            return api.GetMetricSamples(metric_name, start, end, **kwargs)
        elif provider == "google":
            query = f"fetch cloud.googleapis.com/metrics/{metric_name} | within "
            query += f"{start},{end}"
            return self._client.query_time_series(query)
        elif provider == "ibm":
            return self._client.get_metric(metric_name, start, end, **kwargs)
        elif provider == "azure":
            # Azure Monitor returns aggregated results; kwargs can contain aggregation type
            aggregation = kwargs.get("aggregation", "Average")
            result = self._client.timeseries.get(namespace="custom/metrics", metric_names=[metric_name],
                                                 timespan=f"{start}/{end}", interval="PT1M", aggregation=aggregation)
            return result
        elif provider == "aws":
            return self._client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName=metric_name,
                StartTime=start,
                EndTime=end,
                Period=60,
                Statistics=["Average"],
                **kwargs)
        elif provider == "alibaba":
            # Alibaba CloudMonitor uses a generic get_metric_data call
            return self._client.GetMetricData(MetricName=metric_name, StartTime=start, EndTime=end, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_aggregated_stats(self, metric_name: str, start: str, end: str, **kwargs) -> Any:
        """Retrieve aggregated statistics for a metric over a time window.

        Supports provider-specific aggregation (e.g., sum, avg, max).
        """
        provider = os.getenv("MONITORING_PROVIDER", "datadog")
        if provider == "datadog":
            from datadog import api
            return api.GetMetricSamples(metric_name, start, end, aggregate="sum", **kwargs)
        elif provider == "google":
            query = f"fetch cloud.googleapis.com/metrics/{metric_name} | within "
            query += f"{start},{end} | group_by 1m, mean(value)"
            return self._client.query_time_series(query)
        elif provider == "ibm":
            return self._client.get_metric(metric_name, start, end, aggregate="avg", **kwargs)
        elif provider == "azure":
            aggregation = kwargs.get("aggregation", "Average")
            result = self._client.timeseries.get(namespace="custom/metrics", metric_names=[metric_name],
                                                 timespan=f"{start}/{end}", interval="PT1M", aggregation=aggregation)
            return result
        elif provider == "aws":
            return self._client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName=metric_name,
                StartTime=start,
                EndTime=end,
                Period=300,
                Statistics=["Average", "Sum", "Maximum", "Minimum"],
                **kwargs)
        elif provider == "alibaba":
            return self._client.GetMetricData(MetricName=metric_name, StartTime=start, EndTime=end, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def filter_by_dimensions(self, metric_name: str, filter_expr: str, start: str, end: str, **kwargs) -> Any:
        """Query metric data filtered by resource labels or dimensions.

        The `filter_expr` follows the native DSL of the chosen provider.
        """
        provider = os.getenv("MONITORING_PROVIDER", "datadog")
        if provider == "datadog":
            from datadog import api
            # Datadog uses "<metric>.over(<tags>)" syntax
            return api.GetMetricSamples(metric_name, start, end, tags=filter_expr.split(), **kwargs)
        elif provider == "google":
            # Google Cloud Monitoring uses filter string in the read_time_series API
            filter_str = f"resource.type=""gce_instance"" AND metric.type="{metric_name}" AND {filter_expr}"
            return self._client.list_time_series(name="projects/your-project-id", filter=filter_str,
                                                 interval={'startTime': start, 'endTime': end},
                                                 view="FULL")
        elif provider == "ibm":
            # IBM Cloud Monitoring supports label filters via the `labels` param
            return self._client.get_metric(metric_name, start, end, labels=filter_expr, **kwargs)
        elif provider == "azure":
            # Azure uses a OData $filter query parameter
            filter_str = f"{filter_expr}"
            return self._client.timeseries.get(namespace="custom/metrics", metric_names=[metric_name],
                                               timespan=f"{start}/{end}", interval="PT1M", filter=filter_str)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    # ---------------------------------------------------------------------------
    # Local helper utilities (optional, for normalization or response parsing)
    # ---------------------------------------------------------------------------
    def _normalize_response(self, provider: str, raw: Any) -> Any:
        """Convert provider-specific response to a common dict format."""
        if provider == "datadog":
            return {
                "metric": raw[0]["metric"],
                "points": raw[0]["pointlist"],
                "tags": raw[0]["tags"]
            }
        elif provider == "google":
            return [{"timestamp": point.timestamp, "value": point.value} for point in raw]
        elif provider == "ibm":
            return {
                "metric": raw["metric"],
                "samples": raw["samples"]
            }
        elif provider == "azure":
            return [{"time": dp.timestamp, "value": dp.value} for dp in raw]
        elif provider == "aws":
            return {
                "metric": raw["Label"],
                "datapoints": raw["Datapoints"]
            }
        elif provider == "alibaba":
            return {
                "metric": raw["MetricName"],
                "datapoints": raw["Values"]
            }
        return raw
