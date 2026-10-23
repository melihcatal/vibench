from typing import List, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str
    context_documents: Optional[List[str]] = Field(default_factory=list)
    model: str = "command-r"

class SummaryResponse(BaseModel):
    summary: str
    id: str

class StreamedChatResponse:
    def __init__(self, stream):
        self.stream = stream

    def __iter__(self):
        for event in self.stream:
            if event.event_type == "text-generation":
                yield event.text

    def get_final_response(self):
        return self.stream.get_final_response()
