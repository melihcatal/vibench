from __future__ import annotations

from document_client import DEFAULT_MODEL_DOCUMENT, OCRClientFactory, load_bytes
from document_models import KeyValueExtractionResult, KeyValueModel, to_bounding_regions


def extract_key_values(document_path: str) -> KeyValueExtractionResult:
    client = OCRClientFactory().create_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_MODEL_DOCUMENT,
        body=load_bytes(document_path),
        content_type="application/octet-stream",
    )
    result = poller.result()
    pairs = []
    for item in result.key_value_pairs or []:
        key_content = item.key.content if item.key else ""
        value_content = item.value.content if item.value else ""
        confidence = getattr(item, "confidence", None)
        regions = []
        if item.key:
            regions.extend(to_bounding_regions(getattr(item.key, "bounding_regions", None)))
        if item.value:
            regions.extend(to_bounding_regions(getattr(item.value, "bounding_regions", None)))
        pairs.append(
            KeyValueModel(
                key=key_content,
                value=value_content,
                confidence=confidence,
                bounding_regions=regions,
            )
        )
    return KeyValueExtractionResult(pairs=pairs, model_id=DEFAULT_MODEL_DOCUMENT)
