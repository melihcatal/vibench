import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def conditional_update(document_id, update, condition):
    response = client.documents.update(
        database_id='my-database-id',
        document_id=document_id,
        update=update,
        condition=condition
    )
    return response