import os
from typing import Optional
from alibabacloud_ocr_api20210707.models import RecognizeKeyValuesRequest
from document_client import create_ocr_client, encode_image_to_base64
from document_models import DocumentKeyValueResult, KeyValue


def extract_key_values_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> DocumentKeyValueResult:
    client = create_ocr_client()
    image_base64 = encode_image_to_base64(image_path, image_bytes)

    request = RecognizeKeyValuesRequest(body=image_base64)
    response = client.recognize_key_values(request)

    body = response.body
    key_values = []

    if hasattr(body, "data") and body.data:
        data = body.data
        if isinstance(data, dict):
            for kv_data in data.get("key_values", []):
                kv = KeyValue(
                    key=kv_data.get("key", ""),
                    value=kv_data.get("value", ""),
                    confidence=kv_data.get("confidence", 0.0),
                )
                key_values.append(kv)

    return DocumentKeyValueResult(key_values=key_values, page_count=1)


if __name__ == "__main__":
    image_file = os.environ.get("DOCUMENT_IMAGE_PATH")
    if image_file:
        result = extract_key_values_from_image(image_path=image_file)
        for kv in result.key_values:
            print(f"{kv.key}: {kv.value} (confidence: {kv.confidence})")
