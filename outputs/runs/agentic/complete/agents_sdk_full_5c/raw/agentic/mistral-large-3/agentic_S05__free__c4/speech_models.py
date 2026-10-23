from pydantic import BaseModel
from typing import Optional

class TranscriptEvent(BaseModel):
    text: str
    is_final: bool
    language: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    @classmethod
    def from_openai_response(cls, response):
        return cls(
            text=response.get("text", ""),
            is_final=response.get("is_final", False),
            language=response.get("language"),
        )