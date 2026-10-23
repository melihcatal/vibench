import os

from amazon_nova_api import NovaDocumentClient


def get_document_client():
    api_key = os.getenv('NOVA_API_KEY')
    client = NovaDocumentClient(api_key=api_key)
    return client


def extract_document(document_id):
    client = get_document_client()
    document = client.extract(document_id)
    return document
