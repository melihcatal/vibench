class DocumentRequest:
    def __init__(self, id, data):
        self.id = id
        self.data = data

class DocumentResponse:
    def __init__(self, id, data):
        self.id = id
        self.data = data

def normalize_request(request):
    return {
        'id': request.id,
        'data': request.data
    }

def normalize_response(response):
    return DocumentResponse(response['id'], response['data'])