from typing import List, Dict, Any, Optional

class LLMRequest:
    text: str
    model_id: str
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None

    def __init__(self, text: str, model_id: str, max_output_tokens: Optional[int] = None, temperature: Optional[float] = None, top_p: Optional[float] = None, top_k: Optional[int] = None):
        self.text = text
        self.model_id = model_id
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k

class LLMResponse:
    generated_text: str
    raw_response: Dict[str, Any]

    def __init__(self, generated_text: str, raw_response: Dict[str, Any]):
        self.generated_text = generated_text
        self.raw_response = raw_response

class ContextualLLMRequest(LLMRequest):
    context: str

    def __init__(self, text: str, context: str, model_id: str, max_output_tokens: Optional[int] = None, temperature: Optional[float] = None, top_p: Optional[float] = None, top_k: Optional[int] = None):
        super().__init__(text, model_id, max_output_tokens, temperature, top_p, top_k)
        self.context = context
