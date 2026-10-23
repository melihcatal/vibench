class DocumentRequest:
    def __init__(self, document_bytes):
        self.document_bytes = document_bytes

class DocumentResponse:
    def __init__(self, response):
        self.response = response

def normalize_response(response):
    normalized_response = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = block.get('Relationships', [])[0].get('Text')
            normalized_response[key] = value
    return normalized_response