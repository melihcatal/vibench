class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, toxic_content_detected, toxicity_score):
        self.toxic_content_detected = toxic_content_detected
        self.toxicity_score = toxicity_score