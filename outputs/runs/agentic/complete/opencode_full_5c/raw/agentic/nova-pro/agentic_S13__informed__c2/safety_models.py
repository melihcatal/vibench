class SafetyRequest:
    def __init__(self, text):
        self.text = text


class SafetyResponse:
    def __init__(self, is_safe, score):
        self.is_safe = is_safe
        self.score = score


def normalize_response(response):
    # Implementation details
    pass
