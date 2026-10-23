from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_document_intelligence_client
from document_models import DocumentInput, KeyValueExtractionResult


def extract_key_values(doc_input: DocumentInput) -> KeyValueExtractionResult:
    client = get_document_intelligence_client()

    if doc_input.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-document", document_url=doc_input.document_url
        )
    elif doc_input.document_bytes and doc_input.content_type:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=doc_input.document_bytes,
            content_type=doc_input.content_type,
        )
    else:
        raise ValueError(
            "Either document_url or document_bytes with content_type must be provided."
        )

    result: AnalyzeResult = poller.result()

    kv_result = KeyValueExtractionResult()

    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            if kvp.key and kvp.value:
                kv_result.key_value_pairs.append(
                    {
                        "key": kvp.key.content,
                        "value": kvp.value.content if kvp.value.content else "",
                        "key_bounding_regions": [
                            br.to_dict() for br in kvp.key.bounding_regions
                        ],
                        "value_bounding_regions": [
                            br.to_dict() for br in kvp.value.bounding_regions
                        ],
                    }
                )

    return kv_result
