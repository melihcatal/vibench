import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def fetch_document(document_id):
    response = client.documents.get(
        database_id='my-database-id',
        document_id=document_id
    )
    return response