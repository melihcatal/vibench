from typing import Dict, Any, List, Union

# Define local request and response models for Hosted LLM Inference and Model-Family Selection
# These are simplified and can be expanded based on specific needs.

class LLMRequest:
    text: str
    model: str
    parameters: Dict[str, Any]

    def __init__(self, text: str, model: str = "gemini-pro", parameters: Dict[str, Any] = None):
        self.text = text
        self.model = model
        self.parameters = parameters if parameters is not None else {}

class LLMResponse:
    text: str
    raw_response: Any

    def __init__(self, text: str, raw_response: Any = None):
        self.text = text
        self.raw_response = raw_response

class LLMStreamResponse:
    chunk: str
    raw_chunk: Any

    def __init__(self, chunk: str, raw_chunk: Any = None):
        self.chunk = chunk
        self.raw_chunk = raw_chunk
