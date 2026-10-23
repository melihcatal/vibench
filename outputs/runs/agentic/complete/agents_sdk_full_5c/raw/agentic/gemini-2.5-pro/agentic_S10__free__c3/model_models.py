from typing import TypedDict, List

class SummaryRequest(TypedDict):
    text: str
    model: str
    length: str
    format: str

class ChatRequest(TypedDict):
    message: str
    model: str

class AnswerWithContextRequest(TypedDict):
    question: str
    documents: List[str]
    model: str
