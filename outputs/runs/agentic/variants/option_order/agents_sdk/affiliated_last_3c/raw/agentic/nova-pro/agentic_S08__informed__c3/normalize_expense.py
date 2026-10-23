import mindee

MINDEE_API_KEY = 'your_mindee_api_key'

def normalize_expense(document_path):
    client = mindee.Client(api_key=MINDEE_API_KEY)
    response = client.document.parse(document_path)
    # Normalize fields from response
    return normalized_fields