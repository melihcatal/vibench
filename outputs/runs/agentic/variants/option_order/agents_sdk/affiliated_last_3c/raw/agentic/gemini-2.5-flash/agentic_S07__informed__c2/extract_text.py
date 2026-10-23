import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def extract_text_from_document(document_path: str) -> str:
    """
    Extracts plain text from a scanned document image using Azure Document Intelligence.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", document=f.read()
        )
        result = poller.result()

    return result.content

if __name__ == '__main__':
    # Example usage (requires environment variables set and a test document)
    # print(extract_text_from_document("path/to/your/document.pdf"))
    pass
