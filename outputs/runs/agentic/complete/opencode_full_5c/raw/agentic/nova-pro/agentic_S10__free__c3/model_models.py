class Request:
    def __init__(self, text):
        self.text = text


class Response:
    def __init__(self, data):
        self.data = data


def normalize_response(response):
    return response[0]["summary_text"]
