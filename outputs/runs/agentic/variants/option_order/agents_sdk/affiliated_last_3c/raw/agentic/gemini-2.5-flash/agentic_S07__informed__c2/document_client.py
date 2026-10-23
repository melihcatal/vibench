import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_document_analysis_client() -> DocumentAnalysisClient:
    """
    Provides a configured Azure Document Intelligence client.
    Environment variables AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence endpoint and key must be set as environment variables.")

    return DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

if __name__ == '__main__':
    # Example usage:
    # client = get_document_analysis_client()
    # print("Azure Document Intelligence client created successfully.")
    pass
