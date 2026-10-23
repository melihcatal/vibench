import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class ObservabilityConfig:
    aws_region: str
    namespace: str
    metric_name: str


class ObservabilityClientFactory:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1'

    def config(self, namespace: str, metric_name: str) -> ObservabilityConfig:
        return ObservabilityConfig(aws_region=self.region_name, namespace=namespace, metric_name=metric_name)

    def cloudwatch(self):
        return boto3.client('cloudwatch', region_name=self.region_name)
