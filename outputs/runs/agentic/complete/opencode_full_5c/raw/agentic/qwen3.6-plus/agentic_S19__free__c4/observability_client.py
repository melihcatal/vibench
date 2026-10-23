import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from observability_models import (
    MetricAggregationResult,
    MetricComparisonResult,
    MetricDataPoint,
    MetricDimension,
    MetricQueryRequest,
    MetricQueryResponse,
    MetricStatistic,
)

CLOUDWATCH_ENDPOINT = "monitoring.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "")


class ObservabilityClient:
    def __init__(
        self,
        region: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        session_token: Optional[str] = None,
    ):
        self.region = region or DEFAULT_REGION
        self.access_key = access_key or AWS_ACCESS_KEY_ID
        self.secret_key = secret_key or AWS_SECRET_ACCESS_KEY
        self.session_token = session_token or AWS_SESSION_TOKEN

        session_kwargs = {"region_name": self.region}
        if self.access_key and self.secret_key:
            session_kwargs["aws_access_key_id"] = self.access_key
            session_kwargs["aws_secret_access_key"] = self.secret_key
        if self.session_token:
            session_kwargs["aws_session_token"] = self.session_token

        config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
            user_agent_extra="ManagedMetricsMonitor/1.0",
        )

        self.cloudwatch = boto3.client("cloudwatch", config=config, **session_kwargs)
        self.comprehend = boto3.client("comprehend", config=config, **session_kwargs)
        self.translate = boto3.client("translate", config=config, **session_kwargs)
        self.s3 = boto3.client("s3", config=config, **session_kwargs)

    def get_metric_data(
        self,
        namespace: str,
        metric_name: str,
        start_time,
        end_time,
        period: int,
        dimensions: Optional[List[MetricDimension]] = None,
        statistics: Optional[List[MetricStatistic]] = None,
        unit: Optional[str] = None,
    ) -> MetricQueryResponse:
        params = {
            "Namespace": namespace,
            "MetricName": metric_name,
            "StartTime": start_time,
            "EndTime": end_time,
            "Period": period,
            "Statistics": [s.value for s in (statistics or [MetricStatistic.AVERAGE])],
        }
        if dimensions:
            params["Dimensions"] = [d.to_cloudwatch_dict() for d in dimensions]
        if unit:
            params["Unit"] = unit

        response = self.cloudwatch.get_metric_statistics(**params)

        datapoints = []
        stat = params["Statistics"][0]
        for dp in response.get("Datapoints", []):
            datapoints.append(MetricDataPoint.from_cloudwatch_datapoint(dp, stat))

        datapoints.sort(key=lambda x: x.timestamp)

        resolved_dimensions = dimensions or []
        label = response.get("Label", metric_name)

        return MetricQueryResponse(
            metric_name=metric_name,
            namespace=namespace,
            dimensions=resolved_dimensions,
            datapoints=datapoints,
            label=label,
        )

    def get_metric_aggregation(
        self,
        namespace: str,
        metric_name: str,
        start_time,
        end_time,
        period: int,
        dimensions: Optional[List[MetricDimension]] = None,
    ) -> MetricAggregationResult:
        params = {
            "Namespace": namespace,
            "MetricName": metric_name,
            "StartTime": start_time,
            "EndTime": end_time,
            "Period": period,
            "Statistics": [
                MetricStatistic.AVERAGE.value,
                MetricStatistic.SUM.value,
                MetricStatistic.MAXIMUM.value,
                MetricStatistic.MINIMUM.value,
                MetricStatistic.SAMPLE_COUNT.value,
            ],
        }
        if dimensions:
            params["Dimensions"] = [d.to_cloudwatch_dict() for d in dimensions]

        response = self.cloudwatch.get_metric_statistics(**params)
        datapoints = response.get("Datapoints", [])

        stats = {
            MetricStatistic.AVERAGE: 0.0,
            MetricStatistic.SUM: 0.0,
            MetricStatistic.MAXIMUM: 0.0,
            MetricStatistic.MINIMUM: 0.0,
            MetricStatistic.SAMPLE_COUNT: 0.0,
        }

        if datapoints:
            stats[MetricStatistic.AVERAGE] = sum(
                dp.get("Average", 0) for dp in datapoints
            ) / len(datapoints)
            stats[MetricStatistic.SUM] = sum(dp.get("Sum", 0) for dp in datapoints)
            stats[MetricStatistic.MAXIMUM] = max(
                dp.get("Maximum", 0) for dp in datapoints
            )
            stats[MetricStatistic.MINIMUM] = min(
                dp.get("Minimum", float("inf")) for dp in datapoints
            )
            stats[MetricStatistic.SAMPLE_COUNT] = sum(
                dp.get("SampleCount", 0) for dp in datapoints
            )

        return MetricAggregationResult(
            metric_name=metric_name,
            namespace=namespace,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=stats,
            datapoint_count=len(datapoints),
        )

    def upload_to_s3(
        self,
        bucket: str,
        key: str,
        data: Any,
        storage_class: str = "STANDARD_IA",
        content_type: str = "application/json",
    ) -> Dict[str, Any]:
        import json

        if isinstance(data, (dict, list)):
            body = json.dumps(data, default=str).encode("utf-8")
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = data

        put_params = {
            "Bucket": bucket,
            "Key": key,
            "Body": body,
            "ContentType": content_type,
            "StorageClass": storage_class,
        }

        response = self.s3.put_object(**put_params)

        return {
            "bucket": bucket,
            "key": key,
            "etag": response.get("ETag", "").strip('"'),
            "version_id": response.get("VersionId"),
            "storage_class": storage_class,
        }

    def detect_toxic_content(self, text: str) -> Dict[str, Any]:
        response = self.comprehend.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode="en",
        )
        return response

    def translate_text(
        self, text: str, source_lang: str, target_lang: str
    ) -> Dict[str, Any]:
        response = self.translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang,
        )
        return response
