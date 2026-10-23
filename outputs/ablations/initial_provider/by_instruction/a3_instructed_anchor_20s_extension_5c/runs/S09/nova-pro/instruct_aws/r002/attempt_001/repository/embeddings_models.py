class EmbeddingRequest:
    def __init__(self, text):
        self.text = text

class EmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding

def normalize_payload(request):
    return {'text': request.text}

def parse_response(response):
    return response['body'].read().decode('utf-8')