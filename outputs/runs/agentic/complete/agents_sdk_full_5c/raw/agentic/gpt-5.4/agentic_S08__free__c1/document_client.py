from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from google.cloud import translate_v2 as translate
from google.cloud import firestore


class AzureDocumentConfig:
    def __init__(self) -> None:
        self.endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENDPOINT") or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY") or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure Document Intelligence configuration is missing")


def get_document_analysis_client() -> DocumentAnalysisClient:
    cfg = AzureDocumentConfig()
    return DocumentAnalysisClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.api_key))


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")
    return OpenAI(api_key=api_key)


def get_openai_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def post_openai_responses(payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers=get_openai_headers(),
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def get_translate_client() -> translate.Client:
    return translate.Client()


def get_firestore_client() -> firestore.Client:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    return firestore.Client(project=project) if project else firestore.Client()


def first_content_text(response_json: Dict[str, Any]) -> Optional[str]:
    for output in response_json.get("output", []):
        for content in output.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                return content.get("text")
    return response_json.get("output_text")
