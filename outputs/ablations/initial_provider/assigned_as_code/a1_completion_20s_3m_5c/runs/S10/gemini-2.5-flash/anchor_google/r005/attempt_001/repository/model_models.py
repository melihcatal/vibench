from typing import Dict, Any, List


class TextPayload:
    def __init__(self, text: str):
        self.text = text


class SummaryResult:
    def __init__(self, text: str):
        self.text = text


class JsonExtractionResult:
    def __init__(self, json_data: Dict[str, Any]):
        self.json_data = json_data


class AnswerWithContextPayload:
    def __init__(self, question: str, context: str):
        self.question = question
        self.context = context


class CompletionStreamResult:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
