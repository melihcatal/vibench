from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


def extract_fields(document_path):
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-document", document_file)
        result = poller.result()
        return result.fields
