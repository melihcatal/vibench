class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, sentiment, sentiment_score):
        self.sentiment = sentiment
        self.sentiment_score = sentiment_score
