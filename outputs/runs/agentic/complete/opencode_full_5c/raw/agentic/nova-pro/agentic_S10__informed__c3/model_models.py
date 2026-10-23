class Request:
    def __init__(self, text):
        self.text = text


class Response:
    def __init__(self, summary):
        self.summary = summary


def normalize_response(response):
    return {"summary": response.summary}
