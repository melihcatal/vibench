import os
from dataclasses import dataclass
import boto3


@dataclass(frozen=True)
class ObservabilityConfig:
    namespace: str
    region_name: str | None = None


def load_observability_config():
    return ObservabilityConfig(namespace=os.environ.get('CW_NAMESPACE', 'ManagedMetrics/Monitoring'), region_name=os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION'))


def get_metrics_client(cfg):
    return boto3.client('cloudwatch', region_name=cfg.region_name)
