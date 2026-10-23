class SafetyRequest:
    def __init__(self, text):
        self.text = text

class SafetyResponse:
    def __init__(self, flagged, score):
        self.flagged = flagged
        self.score = score