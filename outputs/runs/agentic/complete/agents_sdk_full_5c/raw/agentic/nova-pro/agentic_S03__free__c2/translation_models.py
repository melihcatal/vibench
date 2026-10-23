class TranslationRequest:
    def __init__(self, text, target_lang='EN'):
        self.text = text
        self.target_lang = target_lang

class TranslationResponse:
    def __init__(self, text):
        self.text = text