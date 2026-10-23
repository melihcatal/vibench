from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_document_intelligence_client
from document_models import DocumentInput, TextExtractionResult


def extract_text(doc_input: DocumentInput) -> TextExtractionResult:
    client = get_document_intelligence_client()

    if doc_input.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-read", document_url=doc_input.document_url
        )
    elif doc_input.document_bytes and doc_input.content_type:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=doc_input.document_bytes,
            content_type=doc_input.content_type,
        )
    else:
        raise ValueError(
            "Either document_url or document_bytes with content_type must be provided."
        )

    result: AnalyzeResult = poller.result()
    return TextExtractionResult(text_content=result.content if result.content else "")
