from pydantic import BaseModel

class LLMRequest(BaseModel):
    model_id: str
    prompt: str
    max_tokens: int

class LLMResponse(BaseModel):
    output_text: str