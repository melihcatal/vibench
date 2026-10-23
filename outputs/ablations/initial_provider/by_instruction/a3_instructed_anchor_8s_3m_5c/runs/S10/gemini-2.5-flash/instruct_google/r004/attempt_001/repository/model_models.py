from typing import Dict, Any, List, Optional

class LLMRequest:
    prompt: str
    model_name: str
    temperature: float
    max_output_tokens: int

    def __init__(self, prompt: str, model_name: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024):
        self.prompt = prompt
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

class LLMResponse:
    text: str
    finish_reason: str
    usage_metadata: Dict[str, Any]

    def __init__(self, text: str, finish_reason: str = "STOP", usage_metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.finish_reason = finish_reason
        self.usage_metadata = usage_metadata if usage_metadata is not None else {}

class JSONExtractionResponse(LLMResponse):
    extracted_json: Dict[str, Any]

    def __init__(self, text: str, extracted_json: Dict[str, Any], finish_reason: str = "STOP", usage_metadata: Optional[Dict[str, Any]] = None):
        super().__init__(text, finish_reason, usage_metadata)
        self.extracted_json = extracted_json

