from pydantic import BaseModel
from typing import Dict, Any


class Prompt(BaseModel):
    text: str


class Response(BaseModel):
    text: str


class JsonPrompt(BaseModel):
    text: str
    json_schema: Dict[str, Any]


class ContextualPrompt(BaseModel):
    question: str
    context: str
