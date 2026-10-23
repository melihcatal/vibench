class TranslationRequest:
    def __init__(self, text, to_language):
        self.text = text
        self.to_language = to_language

class TranslationResponse:
    def __init__(self, text):
        self.text = text

def normalize_response(response):
    return TranslationResponse(response.translations[0].text)