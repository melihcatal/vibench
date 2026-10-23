class ModerationRequest:
    def __init__(self, text):
        self.text = text

class ModerationResponse:
    def __init__(self, score, magnitude):
        self.score = score
        self.magnitude = magnitude

def normalize_response(response):
    return ModerationResponse(response.document_sentiment.score, response.document_sentiment.magnitude)