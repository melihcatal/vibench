import os
from azure.ai.translation.document.models import DocumentTranslationInput, DocumentTranslationInputKind
from azure.ai.translation.document import DocumentTranslationClient

# Configuration
subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
endpoint = os.getenv('AZURE_ENDPOINT')

# Client
client = DocumentTranslationClient(endpoint, AzureKeyCredential(subscription_key))