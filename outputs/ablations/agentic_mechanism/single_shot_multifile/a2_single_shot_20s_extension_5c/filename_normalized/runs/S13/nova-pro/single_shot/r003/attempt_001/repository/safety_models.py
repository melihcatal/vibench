class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, is_safe):
        self.is_safe = is_safe

def normalize_response(response):
    return SafetyResponse(response.document_sentiment.score >= -0.2)
