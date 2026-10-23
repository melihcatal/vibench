from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from document_client import get_document_client, AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
from document_models import (
    DocumentRequest,
    KeyValueResult,
    KeyValuePair,
    BoundingBox,
    normalize_confidence,
    normalize_bounding_box,
)

AZURE_KEY_VALUE_MODEL_ID = "prebuilt-document"


def extract_key_values_from_document(
    request: DocumentRequest,
    client: DocumentIntelligenceClient | None = None,
) -> KeyValueResult:
    if client is None:
        client = get_document_client()

    doc_bytes = request.read_bytes()

    poller = client.begin_analyze_document(
        model_id=AZURE_KEY_VALUE_MODEL_ID,
        body={
            "base64Source": __import__("base64").b64encode(doc_bytes).decode("utf-8")
        },
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    pairs: list[KeyValuePair] = []

    key_value_pairs = result.key_value_pairs or []
    for kv in key_value_pairs:
        key_text = ""
        value_text = ""
        key_confidence = 0.0
        value_confidence = 0.0
        key_bbox = None
        value_bbox = None

        if kv.key:
            key_text = kv.key.content or ""
            key_confidence = normalize_confidence(kv.key.confidence)
            key_bbox = (
                normalize_bounding_box(kv.key.bounding_regions[0].polygon)
                if kv.key.bounding_regions
                else None
            )

        if kv.value:
            value_text = kv.value.content or ""
            value_confidence = normalize_confidence(kv.value.confidence)
            value_bbox = (
                normalize_bounding_box(kv.value.bounding_regions[0].polygon)
                if kv.value.bounding_regions
                else None
            )

        confidence = normalize_confidence(kv.confidence)

        pairs.append(
            KeyValuePair(
                key=key_text,
                value=value_text,
                confidence=confidence,
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
            )
        )

    return KeyValueResult(
        pairs=pairs,
        page_number=1,
    )


def extract_key_values_from_file(
    file_path: str,
    content_type: str = "application/pdf",
) -> KeyValueResult:
    request = DocumentRequest.from_file(file_path, content_type)
    return extract_key_values_from_document(request)


def extract_key_values_from_url(
    url: str,
    client: DocumentIntelligenceClient | None = None,
) -> KeyValueResult:
    if client is None:
        client = get_document_client()

    poller = client.begin_analyze_document(
        model_id=AZURE_KEY_VALUE_MODEL_ID,
        body={"urlSource": url},
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    pairs: list[KeyValuePair] = []

    for kv in result.key_value_pairs or []:
        key_text = ""
        value_text = ""
        key_bbox = None
        value_bbox = None

        if kv.key:
            key_text = kv.key.content or ""
            key_bbox = (
                normalize_bounding_box(kv.key.bounding_regions[0].polygon)
                if kv.key.bounding_regions
                else None
            )

        if kv.value:
            value_text = kv.value.content or ""
            value_bbox = (
                normalize_bounding_box(kv.value.bounding_regions[0].polygon)
                if kv.value.bounding_regions
                else None
            )

        pairs.append(
            KeyValuePair(
                key=key_text,
                value=value_text,
                confidence=normalize_confidence(kv.confidence),
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
            )
        )

    return KeyValueResult(
        pairs=pairs,
        page_number=1,
    )
