from typing import List
from document_client import get_document_analysis_client
from document_models import KeyValue


def extract_key_values_from_document(
    file_path: str = None, url: str = None
) -> List[KeyValue]:
    client = get_document_analysis_client()

    poller = None
    if url:
        poller = client.begin_analyze_document("prebuilt-invoice", {"urlSource": url})
    elif file_path:
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-invoice", f.read())
    else:
        raise ValueError("Either file_path or url must be provided.")

    result = poller.result()

    key_values = []
    if result.documents:
        for doc in result.documents:
            if doc.fields:
                for name, field in doc.fields.items():
                    key_values.append(
                        KeyValue(
                            key=name,
                            value=field.value if field.value else None,
                            confidence=field.confidence if field.confidence else 0.0,
                        )
                    )
    return key_values
