import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def query_documents(field_value):
    response = client.documents.query(
        database_id='my-database-id',
        query={'field': field_value}
    )
    return response