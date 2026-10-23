import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

def extract_key_value_pairs(document_path: str):
    """
    Extracts key-value pairs from a form-like document using Azure Document Intelligence.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.")

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Using 'prebuilt-document' model for general document processing, which can extract KVs
    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-document", analyze_request=f, content_type="application/octet-stream"
        )
        result: AnalyzeResult = poller.result()

    key_value_pairs = {}
    if result.key_value_pairs:
        for kv in result.key_value_pairs:
            if kv.key and kv.value:
                key_value_pairs[kv.key.content] = kv.value.content
    return key_value_pairs

if __name__ == "__main__":
    # Example usage (requires a document_path and environment variables set)
    # kvs = extract_key_value_pairs("path/to/your/form.pdf")
    # print(kvs)
    pass
