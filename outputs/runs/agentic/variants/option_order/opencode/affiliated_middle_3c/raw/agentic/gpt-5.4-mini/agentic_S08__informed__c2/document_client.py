import os


def get_azure_document_intelligence_client():
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_document_bytes(source):
    if hasattr(source, "read"):
        return source.read()
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    with open(source, "rb") as handle:
        return handle.read()
