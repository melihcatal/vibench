class SpeechRequest:
    def __init__(self, language='en-US'):
        self.language = language

class SpeechResponse:
    def __init__(self, result):
        self.result = result

    def get_text(self):
        return self.result.text

def normalize_response(response):
    return SpeechResponse(response)