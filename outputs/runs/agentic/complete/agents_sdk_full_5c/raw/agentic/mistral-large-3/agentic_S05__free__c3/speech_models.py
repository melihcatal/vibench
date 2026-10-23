from pydantic import BaseModel

class PartialResult(BaseModel):
    text: str

class FinalResult(BaseModel):
    text: str

class SpeechConfig(BaseModel):
    model: str = "whisper-1"
    language: str = "en"
    response_format: str = "text"
    punctuation: bool = True