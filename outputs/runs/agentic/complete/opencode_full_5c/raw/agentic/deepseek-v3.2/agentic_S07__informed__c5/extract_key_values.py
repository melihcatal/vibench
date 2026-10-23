import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_client
from document_models import KeyValuePair, BoundingBox


def extract_key_values_from_image(image_path: str) -> list[KeyValuePair]:
    """Extract key-value pairs from a form-like document using Azure Document Intelligence."""
    client = get_document_client()

    with open(image_path, "rb") as f:
        image_data = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=image_data,
        content_type="application/octet-stream",
    )

    result = poller.result()

    key_values = []

    if hasattr(result, "key_value_pairs"):
        for kv in result.key_value_pairs:
            key_text = ""
            value_text = ""
            key_bbox = None
            value_bbox = None

            if kv.key:
                key_text = kv.key.content
                if kv.key.bounding_regions:
                    key_bbox = BoundingBox(
                        x=kv.key.bounding_regions[0].polygon[0].x,
                        y=kv.key.bounding_regions[0].polygon[0].y,
                        width=kv.key.bounding_regions[0].polygon[2].x
                        - kv.key.bounding_regions[0].polygon[0].x,
                        height=kv.key.bounding_regions[0].polygon[2].y
                        - kv.key.bounding_regions[0].polygon[0].y,
                    )

            if kv.value:
                value_text = kv.value.content
                if kv.value.bounding_regions:
                    value_bbox = BoundingBox(
                        x=kv.value.bounding_regions[0].polygon[0].x,
                        y=kv.value.bounding_regions[0].polygon[0].y,
                        width=kv.value.bounding_regions[0].polygon[2].x
                        - kv.value.bounding_regions[0].polygon[0].x,
                        height=kv.value.bounding_regions[0].polygon[2].y
                        - kv.value.bounding_regions[0].polygon[0].y,
                    )

            key_value = KeyValuePair(
                key=key_text,
                value=value_text,
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
                confidence=kv.confidence if hasattr(kv, "confidence") else 1.0,
            )
            key_values.append(key_value)

    return key_values


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_key_values.py <image_path>")
        sys.exit(1)

    key_values = extract_key_values_from_image(sys.argv[1])
    for kv in key_values:
        print(f"{kv.key}: {kv.value} (confidence: {kv.confidence:.2f})")
