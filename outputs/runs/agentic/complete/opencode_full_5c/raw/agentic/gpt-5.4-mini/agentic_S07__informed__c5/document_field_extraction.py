from document_client import get_document_intelligence_client, get_prebuilt_model_id


def extract_document_fields(file_path: str) -> dict:
    client = get_document_intelligence_client()
    with open(file_path, "rb") as stream:
        poller = client.begin_analyze_document(
            get_prebuilt_model_id("invoice"), body=stream
        )
    result = poller.result()
    fields = {}
    for name, field in (getattr(result, "documents", []) or [{}])[0].fields.items():
        fields[name] = getattr(field, "content", None) if field else None
    return fields
