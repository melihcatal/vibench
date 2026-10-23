from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import monitoring_v3, storage
from google.cloud.monitoring_v3.services.metric_service.transports import MetricServiceGrpcTransport
from google.cloud.translate_v3 import TranslationServiceClient
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.vision_models import ImageTextModel


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    region: str
    gcp_location: str
    bucket_name: Optional[str]
    translate_parent: str
    vertex_project: str
    vertex_location: str


def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    region = os.environ.get("GOOGLE_CLOUD_REGION", "global")
    gcp_location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    bucket_name = os.environ.get("METRICS_EXPORT_BUCKET")
    translate_parent = f"projects/{project_id}/locations/{gcp_location}" if project_id else ""
    vertex_project = project_id
    vertex_location = os.environ.get("VERTEX_AI_LOCATION", gcp_location or "us-central1")
    return ObservabilityConfig(
        project_id=project_id,
        region=region,
        gcp_location=gcp_location,
        bucket_name=bucket_name,
        translate_parent=translate_parent,
        vertex_project=vertex_project,
        vertex_location=vertex_location,
    )


@lru_cache(maxsize=1)
def metric_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient(transport=MetricServiceGrpcTransport())


@lru_cache(maxsize=1)
def storage_client() -> storage.Client:
    return storage.Client()


@lru_cache(maxsize=1)
def translate_client() -> TranslationServiceClient:
    return TranslationServiceClient()


@lru_cache(maxsize=1)
def text_generation_model() -> TextGenerationModel:
    return TextGenerationModel.from_pretrained("text-bison@002")


@lru_cache(maxsize=1)
def image_text_model() -> ImageTextModel:
    return ImageTextModel.from_pretrained("imagetext@001")
