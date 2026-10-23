from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

import boto3

from observability_models import MetricWindowRequest, to_epoch_seconds


class CloudWatchObservabilityClient:
    provider = "amazon_cloudwatch"

    def __init__(self, region_name: Optional[str] = None) -> None:
        self.region_name = (
            region_name
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or "us-east-1"
        )
        self.client = boto3.client("cloudwatch", region_name=self.region_name)

    def get_metric_statistics(self, request: MetricWindowRequest) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "Namespace": request.namespace,
            "MetricName": request.metric_name,
            "StartTime": request.start_time,
            "EndTime": request.end_time,
            "Period": request.period,
            "Statistics": [request.stat],
            "Dimensions": request.cloudwatch_dimensions(),
        }
        if request.unit:
            params["Unit"] = request.unit
        return self.client.get_metric_statistics(**params)

    def get_metric_data(
        self,
        namespace: str,
        metric_name: str,
        start_time,
        end_time,
        queries: Iterable[Dict[str, Any]],
        scan_by: str = "TimestampAscending",
    ) -> Dict[str, Any]:
        return self.client.get_metric_data(
            StartTime=start_time,
            EndTime=end_time,
            MetricDataQueries=list(queries),
            ScanBy=scan_by,
        )

    def build_metric_data_query(
        self,
        query_id: str,
        namespace: str,
        metric_name: str,
        dimensions: Optional[Dict[str, str]],
        stat: str,
        period: int,
        label: Optional[str] = None,
    ) -> Dict[str, Any]:
        metric_stat: Dict[str, Any] = {
            "Metric": {
                "Namespace": namespace,
                "MetricName": metric_name,
                "Dimensions": [
                    {"Name": k, "Value": v} for k, v in (dimensions or {}).items()
                ],
            },
            "Period": period,
            "Stat": stat,
        }
        query: Dict[str, Any] = {
            "Id": query_id,
            "MetricStat": metric_stat,
            "ReturnData": True,
        }
        if label:
            query["Label"] = label
        return query

    @staticmethod
    def pack_export_record(
        metric_name: str, namespace: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "provider": "amazon_cloudwatch",
            "namespace": namespace,
            "metric_name": metric_name,
            "exported_at_epoch": to_epoch_seconds(
                __import__("datetime").datetime.utcnow()
            ),
            "payload": payload,
        }


def get_cloudwatch_client(
    region_name: Optional[str] = None,
) -> CloudWatchObservabilityClient:
    return CloudWatchObservabilityClient(region_name=region_name)


def latest_value(series: List[Dict[str, Any]]) -> Optional[float]:
    if not series:
        return None
    return float(series[-1]["value"])
