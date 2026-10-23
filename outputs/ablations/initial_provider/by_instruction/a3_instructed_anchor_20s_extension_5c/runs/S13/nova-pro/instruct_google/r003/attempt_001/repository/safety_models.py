from google.cloud import language_v1

class SafetyRequest:
    def __init__(self, text):
        self.text = text
        self.document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

class SafetyResponse:
    def __init__(self, response):
        self.sentiment_score = response.document_sentiment.score

def normalize_response(response):
    return SafetyResponse(response)
