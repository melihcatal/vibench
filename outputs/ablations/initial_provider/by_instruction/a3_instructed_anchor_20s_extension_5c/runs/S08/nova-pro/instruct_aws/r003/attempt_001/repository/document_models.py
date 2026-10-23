class DocumentRequest:
    def __init__(self, image_bytes):
        self.image_bytes = image_bytes

class DocumentResponse:
    def __init__(self, response):
        self.response = response

def normalize_response(response):
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                fields[block['Text']] = ''
            else:
                fields[list(fields.keys())[-1]] = block['Text']
    return fields