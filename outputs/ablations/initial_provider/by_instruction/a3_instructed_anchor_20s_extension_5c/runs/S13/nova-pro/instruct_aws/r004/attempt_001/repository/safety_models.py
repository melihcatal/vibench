class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, labels):
        self.labels = labels

def normalize_response(response):
    return SafetyResponse(response['Labels'])
