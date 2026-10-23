class Request:
    def __init__(self, text):
        self.text = text


class Response:
    def __init__(self, output):
        self.output = output


def normalize_request(request):
    return request.text


def normalize_response(response):
    return response.output
