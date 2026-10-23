from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

import boto3
from botocore.config import Config
from openai import OpenAI
import requests
from deepl import Translator

from observability_models import (
    MetricPoint,
    MetricWindowRequest,
    ensure_utc,
    isoformat_utc,
)


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def cloudwatch_client():
    return boto3.client(
        "cloudwatch",
        region_name=get_aws_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def s3_client():
    return boto3.client(
        "s3",
        region_name=get_aws_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def deepl_translator() -> Translator:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    return Translator(auth_key)


def perspective_endpoint() -> str:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    return f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"


def perspective_headers() -> dict[str, str]:
    return {"Content-Type": "application/json"}


def fetch_metric_series(request: MetricWindowRequest) -> list[MetricPoint]:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=[
            {"Name": key, "Value": value}
            for key, value in request.normalized_dimensions().items()
        ],
        StartTime=ensure_utc(request.start_time),
        EndTime=ensure_utc(request.end_time),
        Period=request.period,
        Statistics=[request.stat],
    )
    datapoints = sorted(
        response.get("Datapoints", []), key=lambda item: item["Timestamp"]
    )
    points: list[MetricPoint] = []
    for item in datapoints:
        value = item.get(request.stat)
        if value is None:
            continue
        points.append(
            MetricPoint(
                timestamp=isoformat_utc(item["Timestamp"]),
                value=float(value),
                unit=item.get("Unit"),
                dimensions=request.normalized_dimensions(),
            )
        )
    return points


def dumps_json(data: Any) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def post_perspective(text: str) -> dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(
        perspective_endpoint(),
        headers=perspective_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def current_timestamp_key(prefix: str, metric_name: str, exported_at: datetime) -> str:
    safe_metric = metric_name.replace(" ", "_").replace("/", "-")
    return f"{prefix.rstrip('/')}/{safe_metric}-{exported_at.strftime('%Y%m%dT%H%M%SZ')}.json"
