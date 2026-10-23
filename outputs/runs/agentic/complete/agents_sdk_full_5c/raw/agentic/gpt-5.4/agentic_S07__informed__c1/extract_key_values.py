from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_LAYOUT_MODEL, get_document_intelligence_client, load_document_bytes
from document_models import polygon_to_dicts


def extract_key_values(document_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_LAYOUT_MODEL,
        body=load_document_bytes(document_path),
    )
    result = poller.result()

    pairs: List[Dict[str, Any]] = []
    for pair in result.key_value_pairs or []:
        key_region = pair.key.bounding_regions[0] if pair.key and pair.key.bounding_regions else None
        value_region = pair.value.bounding_regions[0] if pair.value and pair.value.bounding_regions else None
        pairs.append({
            "key": pair.key.content if pair.key else "",
            "value": pair.value.content if pair.value else "",
            "page_number": key_region.page_number if key_region else (value_region.page_number if value_region else None),
            "key_polygon": polygon_to_dicts(key_region.polygon if key_region else None),
            "value_polygon": polygon_to_dicts(value_region.polygon if value_region else None),
            "confidence": getattr(pair, "confidence", None),
        })

    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "key_value_pairs": pairs,
    }
