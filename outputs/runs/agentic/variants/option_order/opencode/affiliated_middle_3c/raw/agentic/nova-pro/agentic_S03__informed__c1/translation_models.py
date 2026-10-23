class TranslationRequest:
    def __init__(self, text, source_lang, target_lang):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, text):
        self.text = text


def normalize_response(response):
    return TranslationResponse(response.text)
