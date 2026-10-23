import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import normalize_textract_response, KeyValuePair


def extract_key_values(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Extract key-value pairs from a form-like document using Amazon Textract.

    Args:
        image_path: Path to the image file
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        List of key-value pairs
    """
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Initialize Textract client
    client = DocumentClient(region_name=region)

    # Call Textract API with forms analysis
    response = client.analyze_document(image_bytes, feature_types=["FORMS"])

    # Normalize response
    result = normalize_textract_response(response)

    # Convert to dict format
    key_values = []

    for kv in result.key_value_pairs:
        key_values.append(
            {
                "key": kv.key,
                "value": kv.value,
                "key_confidence": kv.key_confidence,
                "value_confidence": kv.value_confidence,
            }
        )

    return key_values
