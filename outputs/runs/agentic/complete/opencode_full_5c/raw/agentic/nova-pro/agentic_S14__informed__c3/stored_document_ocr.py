from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def stored_document_ocr(document_url):
    client = DocumentIntelligenceClient(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]),
    )
    poller = client.begin_analyze_document(
        "prebuilt-document", document_url=document_url
    )
    result = poller.result()
    print(result)
