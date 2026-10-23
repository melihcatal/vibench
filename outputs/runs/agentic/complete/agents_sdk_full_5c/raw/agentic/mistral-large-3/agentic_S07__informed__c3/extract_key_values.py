from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from typing import List, Dict, Any
import os

from document_client import get_document_intelligence_client
from document_models import KeyValueResponse


def extract_key_values_from_image(image_path: str) -> List[KeyValueResponse]:
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read())
        )

    result = poller.result()

    key_values = []
    for kv_pair in result.key_value_pairs:
        key_values.append(
            KeyValueResponse(
                key=kv_pair.key.content if kv_pair.key else "",
                value=kv_pair.value.content if kv_pair.value else "",
                key_bounding_box=kv_pair.key.bounding_regions[0].polygon if kv_pair.key and kv_pair.key.bounding_regions else None,
                value_bounding_box=kv_pair.value.bounding_regions[0].polygon if kv_pair.value and kv_pair.value.bounding_regions else None,
                confidence=kv_pair.confidence
            )
        )

    return key_values