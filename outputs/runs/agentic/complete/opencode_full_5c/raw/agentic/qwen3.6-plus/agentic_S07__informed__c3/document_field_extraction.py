from document_client import get_azure_document_client, load_image_bytes


def extract_document_fields(image_path: str) -> dict:
    client = get_azure_document_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice", body=image_bytes
    )
    result = poller.result()
    fields = {}
    if result.documents:
        for doc in result.documents:
            for field_name, field_value in doc.fields.items():
                fields[field_name] = {
                    "value": field_value.value
                    if hasattr(field_value, "value")
                    else str(field_value),
                    "confidence": field_value.confidence
                    if hasattr(field_value, "confidence")
                    else 0.0,
                }
    return fields
