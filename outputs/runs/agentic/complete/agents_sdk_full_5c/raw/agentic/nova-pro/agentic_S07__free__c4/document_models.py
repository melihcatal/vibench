class DocumentRequest:
    def __init__(self, bytes):
        self.bytes = bytes

class DocumentResponse:
    def __init__(self, text):
        self.text = text

def normalize_response(response):
    text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return DocumentResponse(text)