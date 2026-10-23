class TextModerationRequest:
    def __init__(self, text):
        self.text = text

class TextModerationResponse:
    def __init__(self, is_safe):
        self.is_safe = is_safe
