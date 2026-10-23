from __future__ import annotations

import os
from typing import Optional

from google.cloud import kms_v1
from google.cloud import kms_inventory_v1
from google.cloud import translate_v2 as translate
from google.cloud import aiplatform_v1
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI


GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_CLOUD_KEY_RING = os.getenv("GOOGLE_CLOUD_KEY_RING")
GOOGLE_CLOUD_KMS_KEY = os.getenv("GOOGLE_CLOUD_KMS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def kms_key_name(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    key_ring: Optional[str] = None,
    crypto_key: Optional[str] = None,
) -> str:
    project = project_id or GOOGLE_CLOUD_PROJECT
    loc = location or GOOGLE_CLOUD_LOCATION
    ring = key_ring or GOOGLE_CLOUD_KEY_RING
    key = crypto_key or GOOGLE_CLOUD_KMS_KEY
    if not all([project, loc, ring, key]):
        raise ValueError("Missing Google Cloud KMS configuration")
    return f"projects/{project}/locations/{loc}/keyRings/{ring}/cryptoKeys/{key}"


def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def get_kms_inventory_client() -> kms_inventory_v1.KeyDashboardServiceClient:
    return kms_inventory_v1.KeyDashboardServiceClient()


def get_translate_client() -> translate.Client:
    return translate.Client()


def get_vertex_prediction_client(location: Optional[str] = None) -> aiplatform_v1.PredictionServiceClient:
    endpoint = f"{location or GOOGLE_CLOUD_LOCATION}-aiplatform.googleapis.com"
    return aiplatform_v1.PredictionServiceClient(client_options={"api_endpoint": endpoint})


def get_openai_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=OPENAI_API_KEY)


def build_aesgcm(key_bytes: bytes) -> AESGCM:
    return AESGCM(key_bytes)
