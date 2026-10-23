class SummarizeResponse:
    def __init__(self, summary):
        self.summary = summary

class ExtractJsonResponse:
    def __init__(self, json_data):
        self.json_data = json_data

class AnswerWithContextResponse:
    def __init__(self, answer):
        self.answer = answer