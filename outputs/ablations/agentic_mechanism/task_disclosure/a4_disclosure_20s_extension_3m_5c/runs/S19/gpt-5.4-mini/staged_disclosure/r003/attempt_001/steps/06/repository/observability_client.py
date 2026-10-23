import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class ManagedMetricsConfig:
    region_name: str = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    namespace: str = os.getenv("MANAGED_METRICS_NAMESPACE", "ManagedMetricsMonitoring")
    service_name: str = os.getenv("MANAGED_METRICS_SERVICE_NAME", "observability")
    environment: str = os.getenv("MANAGED_METRICS_ENVIRONMENT", "local")
    component: str = os.getenv("MANAGED_METRICS_COMPONENT", "client")


class ManagedMetricsClient:
    def __init__(self, config: Optional[ManagedMetricsConfig] = None) -> None:
        self.config = config or ManagedMetricsConfig()
        self._cloudwatch = boto3.client("cloudwatch", region_name=self.config.region_name)

    def put_metric(self, metric_name: str, value: float, unit: str = "Count", dimensions: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        metric_dimensions = [
            {"Name": "Service", "Value": self.config.service_name},
            {"Name": "Environment", "Value": self.config.environment},
            {"Name": "Component", "Value": self.config.component},
        ]
        if dimensions:
            metric_dimensions.extend({"Name": key, "Value": str(val)} for key, val in dimensions.items())
        return self._cloudwatch.put_metric_data(
            Namespace=self.config.namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": float(value),
                    "Unit": unit,
                    "Dimensions": metric_dimensions,
                }
            ],
        )

    def put_latency(self, metric_name: str, milliseconds: float, dimensions: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self.put_metric(metric_name, milliseconds, unit="Milliseconds", dimensions=dimensions)

    def put_count(self, metric_name: str, count: float = 1.0, dimensions: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self.put_metric(metric_name, count, unit="Count", dimensions=dimensions)
