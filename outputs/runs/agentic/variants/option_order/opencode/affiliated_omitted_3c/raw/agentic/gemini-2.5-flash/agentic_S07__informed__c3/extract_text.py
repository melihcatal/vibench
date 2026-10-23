from document_client import get_document_intelligence_client
from document_models import ExtractedText
from azure.ai.documentintelligence.models import DocumentAnalysisFeature


def extract_text_from_document(document_path: str) -> ExtractedText:
    client = get_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read", analyze_request=f, content_type="application/octet-stream"
        )
    result = poller.result()

    full_text = "\n".join([page.content for page in result.pages])

    return ExtractedText(content=full_text)
