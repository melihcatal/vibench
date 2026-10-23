import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

def extract_plain_text(document_path: str) -> str:
    """
    Extracts plain text from a scanned document image using Azure Document Intelligence.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.")

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", analyze_request=f, content_type="application/octet-stream"
        )
        result: AnalyzeResult = poller.result()

    if result.content:
        return result.content
    return ""

if __name__ == "__main__":
    # Example usage (requires a document_path and environment variables set)
    # text = extract_plain_text("path/to/your/document.jpg")
    # print(text)
    pass
