import requests
from document_client import DocumentClient

# Mindee Invoice OCR - concrete provider identified by the request URL
MINDEE_ENDPOINT = 'https://www.mindee.net/document-ocr/api/v4/invoices/infer'

HEADERS = {'Authorization': f'ApiKey {DocumentClient.get_api_key("MINDEE_API_KEY")}'}

def extract_receipt_fields(file_bytes):
    '''Extract merchant, tax, total, and items from a receipt using Mindee Invoice OCR.'''
    response = requests.post(
        MINDEE_ENDPOINT,
        files={'file': ('receipt.jpg', file_bytes, 'application/octet-stream')},
        headers=HEADERS,
        timeout=30
    )
    data = response.json()
    # Simplified extraction - adapt to actual schema returned by Mindee
    merchant = data.get('merchant', {}).get('name')
    tax = data.get('tax_total')
    total = data.get('total')
    items = [item['text'] for item in data.get('items', [])]
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}
