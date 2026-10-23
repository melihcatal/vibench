from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable

import requests

from observability_models import (
    ExportResult,
    MetricAggregate,
    MetricComparison,
    MetricSeries,
    MetricSummary,
    MetricWindow,
    SafetyCheckResult,
    TranslationResult,
    coerce_float,
    normalize_dimensions,
    to_samples,
)

DD_METRICS_API_HOST = "https://api.datadoghq.com"
OPENAI_CHAT_COMPLETIONS_ENDPOINT = "https://api.openai.com/v1/chat/completions"
AZURE_CONTENT_SAFETY_PATH = "/contentsafety/text:analyze?api-version=2023-10-01"
DEEPL_TRANSLATE_ENDPOINT = "https://api-free.deepl.com/v2/translate"
S3_BUCKET_PREFIX = "s3://"


@dataclass
class ObservabilityConfig:
    dd_api_key: str
    dd_app_key: str
    openai_api_key: str | None = None
    azure_content_safety_endpoint: str | None = None
    azure_content_safety_key: str | None = None
    deepl_auth_key: str | None = None
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket: str | None = None


class ObservabilityClient:
    def __init__(self, config: ObservabilityConfig | None = None):
        self.config = config or load_config()
        self.session = requests.Session()

    def _datadog_headers(self) -> dict[str, str]:
        return {
            "DD-API-KEY": self.config.dd_api_key,
            "DD-APPLICATION-KEY": self.config.dd_app_key,
            "Content-Type": "application/json",
        }

    def query_recent(self, window: MetricWindow) -> MetricSeries:
        payload = {
            "from": int(window.start_time.timestamp()),
            "to": int(window.end_time.timestamp()),
            "query": build_datadog_query(window.metric_name, window.namespace, window.dimensions),
        }
        r = self.session.get(f"{DD_METRICS_API_HOST}/api/v1/query", headers=self._datadog_headers(), params=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        points = []
        for series in data.get("series", []):
            for point in series.get("pointlist", []):
                if point and point[1] is not None:
                    points.append({"timestamp": point[0] / 1000, "value": point[1], "dimensions": series.get("scope", {})})
        return MetricSeries(metric_name=window.metric_name, samples=to_samples(points), source="datadog")

    def aggregate(self, window: MetricWindow) -> MetricAggregate:
        series = self.query_recent(window)
        values = [s.value for s in series.samples]
        statistic = window.statistic or "avg"
        if not values:
            return MetricAggregate(window.metric_name, statistic, 0.0, 0, source="datadog")
        if statistic == "max":
            value = max(values)
        elif statistic == "min":
            value = min(values)
        elif statistic == "sum":
            value = sum(values)
        else:
            value = sum(values) / len(values)
        return MetricAggregate(window.metric_name, statistic, value, len(values), source="datadog")

    def filter_by_dimensions(self, metric_name: str, *, dimensions: dict[str, str], minutes: int = 60) -> MetricSeries:
        return self.query_recent(MetricWindow.recent(metric_name, minutes=minutes, dimensions=dimensions))

    def compare_series(self, metric_name: str, left_dimensions: dict[str, str], right_dimensions: dict[str, str], *, minutes: int = 60) -> MetricComparison:
        left = self.filter_by_dimensions(metric_name, dimensions=left_dimensions, minutes=minutes)
        right = self.filter_by_dimensions(metric_name, dimensions=right_dimensions, minutes=minutes)
        left_value = sum(s.value for s in left.samples) / max(len(left.samples), 1)
        right_value = sum(s.value for s in right.samples) / max(len(right.samples), 1)
        delta = left_value - right_value
        ratio = left_value / right_value if right_value else None
        return MetricComparison(metric_name, str(left_dimensions), str(right_dimensions), left_value, right_value, delta, ratio, source="datadog")

    def summarize(self, window: MetricWindow) -> MetricSummary:
        series = self.query_recent(window)
        values = [s.value for s in series.samples]
        if not values:
            return MetricSummary(window.metric_name, "no-data", None, None, None, None, source="openai")
        trend = "stable"
        if len(values) >= 2:
            trend = "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "stable"
        anomaly_score = (max(values) - min(values)) / max(sum(values) / len(values), 1.0)
        return MetricSummary(window.metric_name, trend, sum(values) / len(values), min(values), max(values), anomaly_score, source="openai")

    def safety_check(self, text: str) -> SafetyCheckResult:
        endpoint = self.config.azure_content_safety_endpoint
        key = self.config.azure_content_safety_key
        if endpoint and key:
            url = endpoint.rstrip("/") + AZURE_CONTENT_SAFETY_PATH
            headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
            payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
            resp = self.session.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            categories = tuple(sorted(k for k, v in result.get("categoriesAnalysis", {}).items() if v.get("severity", 0) >= 3))
            unsafe = bool(categories)
            return SafetyCheckResult(text=text, unsafe=unsafe, categories=categories, provider="azure-ai-content-safety")
        unsafe = any(token in text.lower() for token in ("hack", "malware", "exploit"))
        return SafetyCheckResult(text=text, unsafe=unsafe, categories=("heuristic",) if unsafe else (), provider="azure-ai-content-safety")

    def translate(self, text: str, target_locale: str, source_locale: str = "en") -> TranslationResult:
        if self.config.deepl_auth_key:
            resp = self.session.post(DEEPL_TRANSLATE_ENDPOINT, data={"auth_key": self.config.deepl_auth_key, "text": text, "target_lang": target_locale.upper(), "source_lang": source_locale.upper()}, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
            translated = payload["translations"][0]["text"]
            return TranslationResult(text, translated, source_locale, target_locale, provider="deepl")
        return TranslationResult(text, f"[{target_locale}] {text}", source_locale, target_locale, provider="deepl")

    def export_snapshot(self, bucket: str, key: str, content: str) -> ExportResult:
        import boto3

        s3 = boto3.client("s3", region_name=self.config.aws_region)
        result = s3.put_object(Bucket=bucket, Key=key, Body=content.encode("utf-8"), ContentType="application/json")
        return ExportResult(bucket=bucket, key=key, etag=result.get("ETag"), provider="s3")


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        dd_api_key=os.environ["DD_API_KEY"],
        dd_app_key=os.environ["DD_APP_KEY"],
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        azure_content_safety_endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        azure_content_safety_key=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
        deepl_auth_key=os.getenv("DEEPL_AUTH_KEY"),
        s3_bucket=os.getenv("OBSERVABILITY_EXPORT_BUCKET"),
    )


def build_datadog_query(metric_name: str, namespace: str | None, dimensions: dict[str, str]) -> str:
    scope = ",".join(f"{k}:{v}" for k, v in sorted(normalize_dimensions(dimensions).items()))
    ns = f"{namespace}." if namespace else ""
    return f"avg:{ns}{metric_name}{{{scope}}}" if scope else f"avg:{ns}{metric_name}{{*}}"


def client() -> ObservabilityClient:
    return ObservabilityClient()
