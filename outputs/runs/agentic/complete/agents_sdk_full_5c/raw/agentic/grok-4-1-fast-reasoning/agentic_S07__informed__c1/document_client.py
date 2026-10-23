import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
if not endpoint:
    raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT not set")

key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
if not key:
    raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY not set")

document_client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)