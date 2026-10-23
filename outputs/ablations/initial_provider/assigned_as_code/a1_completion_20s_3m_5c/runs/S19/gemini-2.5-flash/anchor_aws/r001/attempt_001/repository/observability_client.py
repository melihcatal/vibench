import os
from typing import Dict, Any

import boto3

class CloudWatchClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("cloudwatch", region_name=self.region_name)

    def get_client(self):
        return self.client

    def get_cloudwatch_config(self, extra_config: Dict[str, Any] = None) -> Dict[str, Any]:
        config = {
            "region": self.region_name,
            "namespace": os.environ.get("CLOUDWATCH_NAMESPACE", "CustomMetrics"),
            "period_seconds": int(os.environ.get("CLOUDWATCH_PERIOD_SECONDS", 60)),
        }
        if extra_config:
            config.update(extra_config)
        return config
