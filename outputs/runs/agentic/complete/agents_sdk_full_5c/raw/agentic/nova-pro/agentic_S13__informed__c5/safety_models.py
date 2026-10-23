class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, result):
        self.result = result

def normalize_response(response):
    return SafetyResponse(response)
