class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, entities):
        self.entities = entities

def normalize_response(response):
    return SafetyResponse(response['Entities'])