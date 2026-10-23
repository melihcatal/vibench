from typing import List

from document_client import get_azure_document_intelligence_client
from document_models import KeyValuePair


def extract_key_values_from_form(document_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form document using Azure Document Intelligence.
    """
    document_intelligence_client = get_azure_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-document", document=f
        )
    result = poller.result()

    key_value_pairs: List[KeyValuePair] = []

    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_value_pairs.append(
                    KeyValuePair(
                        key=kv_pair.key.content,
                        key_polygon=[
                            p
                            for point in kv_pair.key.bounding_regions[0].polygon
                            for p in (point.x, point.y)
                        ],
                        value=kv_pair.value.content,
                        value_polygon=[
                            p
                            for point in kv_pair.value.bounding_regions[0].polygon
                            for p in (point.x, point.y)
                        ],
                        confidence=kv_pair.confidence,
                    )
                )
            elif kv_pair.key:
                key_value_pairs.append(
                    KeyValuePair(
                        key=kv_pair.key.content,
                        key_polygon=[
                            p
                            for point in kv_pair.key.bounding_regions[0].polygon
                            for p in (point.x, point.y)
                        ],
                        value=None,
                        value_polygon=None,
                        confidence=kv_pair.confidence,
                    )
                )

    return key_value_pairs
