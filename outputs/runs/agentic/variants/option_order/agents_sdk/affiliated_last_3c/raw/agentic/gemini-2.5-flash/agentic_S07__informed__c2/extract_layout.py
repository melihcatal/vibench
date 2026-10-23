import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict

def extract_layout_elements(document_path: str) -> Dict:
    """
    Extracts blocks, lines, and other layout elements from a document using Azure Document Intelligence.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f.read()
        )
        result = poller.result()

    layout_data = {
        "content": result.content,
        "paragraphs": [{"content": p.content, "bounding_regions": p.bounding_regions} for p in result.paragraphs],
        "lines": [{"content": l.content, "bounding_regions": l.bounding_regions} for l in result.pages[0].lines] if result.pages else []
    }
    return layout_data

if __name__ == '__main__':
    # Example usage (requires environment variables set and a test document)
    # layout = extract_layout_elements("path/to/your/document.pdf")
    # print(layout)
    pass
