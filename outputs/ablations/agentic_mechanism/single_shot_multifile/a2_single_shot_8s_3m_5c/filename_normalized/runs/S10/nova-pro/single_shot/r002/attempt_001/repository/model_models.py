class SummarizeResponse:
    def __init__(self, summary):
        self.summary = summary

class ExtractJsonResponse:
    def __init__(self, json):
        self.json = json

class AnswerWithContextResponse:
    def __init__(self, answer):
        self.answer = answer