from pydantic import BaseModel, Field, ValidationError, Extra

# Request models


class ChatRequest(BaseModel):
    model: str = Field(..., description="Model identifier (e.g., gpt-4o)")
    messages: list[dict] = Field(..., description="List of message objects")
    temperature: float = Field(0.0, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(1024, ge=1, description="Maximum token limit")
    stream: bool = Field(False, description="Enable streaming")
    system: str = Field(default="", description="Optional system message")

    class Config:
        extra = Extra.allow


# Response models


class ChatResponse(BaseModel):
    id: str = Field(..., description="Unique request identifier")
    choices: list[dict] = Field(..., description="List of generated choices")
    usage: dict = Field(..., description="Token usage statistics")

    class Config:
        extra = Extra.allow

    def get_text(self) -> str:
        """Extract the raw textual content from the first choice."""
        try:
            return self.choices[0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("Invalid response format")


# Normalization helpers


def normalize_request(request: dict) -> ChatRequest:
    """Convert raw request dict to validated ChatRequest."""
    try:
        return ChatRequest(**request)
    except ValidationError as e:
        raise ValueError(f"Invalid request payload: {e}")


def normalize_response(response: dict) -> ChatResponse:
    """Convert raw response dict to validated ChatResponse."""
    try:
        return ChatResponse(**response)
    except ValidationError as e:
        raise ValueError(f"Invalid response payload: {e}")
