from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class Message(BaseModel):
    role: str
    content: str

class ModelRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Choice(BaseModel):
    message: Dict[str, str]
    finish_reason: str

class ModelResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: Optional[str] = None