from typing import List
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from document_client import get_document_client
from document_models import KeyValuePair, BoundingBox, Point

def extract_key_values_from_url(document_url: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document using Azure AI Document Intelligence.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of KeyValuePair objects found in the document.
    """
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-document", AnalyzeDocumentRequest(url_source=document_url)
    )
    result = poller.result()

    pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_content = kv_pair.key.content if kv_pair.key else ""
            value_content = kv_pair.value.content if kv_pair.value else ""
            
            # Combine bounding boxes of key and value if both exist
            if kv_pair.key and kv_pair.key.bounding_regions and kv_pair.value and kv_pair.value.bounding_regions:
                key_poly = kv_pair.key.bounding_regions[0].polygon
                val_poly = kv_pair.value.bounding_regions[0].polygon
                
                min_x = min(p.x for p in key_poly + val_poly)
                min_y = min(p.y for p in key_poly + val_poly)
                max_x = max(p.x for p in key_poly + val_poly)
                max_y = max(p.y for p in key_poly + val_poly)
                
                points = (Point(min_x, min_y), Point(max_x, min_y), Point(max_x, max_y), Point(min_x, max_y))
                bounding_box = BoundingBox(points=points)

                pairs.append(KeyValuePair(
                    key=key_content,
                    value=value_content,
                    confidence=kv_pair.confidence,
                    bounding_box=bounding_box
                ))

    return pairs
