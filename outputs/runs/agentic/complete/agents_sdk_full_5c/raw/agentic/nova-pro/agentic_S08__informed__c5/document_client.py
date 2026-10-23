import os
from azure.ai.documentintelligence import DocumentIntelligenceClient

client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))