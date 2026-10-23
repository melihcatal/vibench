import os
from azure.identity import DefaultAzureCredential
from azure.ai.translation.document import DocumentTranslationClient

# Set up Azure credentials
credential = DefaultAzureCredential()

# Initialize the client
client = DocumentTranslationClient(endpoint=os.getenv('AZURE_TRANSLATE_ENDPOINT'), credential=credential)