class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, categories, score):
        self.categories = categories
        self.score = score