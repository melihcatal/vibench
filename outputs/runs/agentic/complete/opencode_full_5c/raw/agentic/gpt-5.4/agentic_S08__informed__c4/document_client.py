from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from pymongo import MongoClient
import requests


AZURE_DOCUMENT_INTELLIGENCE_MODEL = "prebuilt-invoice"
OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"
OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def read_binary(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def to_base64_content(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = _require_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = _require_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_invoice_document(data: bytes) -> Any:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(AZURE_DOCUMENT_INTELLIGENCE_MODEL, body=data)
    return poller.result()


def get_openai_client() -> OpenAI:
    api_key = _require_env("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def get_mongodb_client() -> MongoClient:
    uri = _require_env("MONGODB_ATLAS_URI")
    return MongoClient(uri)


def get_perspective_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def analyze_perspective_text(
    text: str, attributes: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    api_key = _require_env("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": attributes
        or {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        headers=get_perspective_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
