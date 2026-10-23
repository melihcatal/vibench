from typing import Dict, Any, List

class LLMRequest:
    """
    Defines a generic request structure for LLM inference.
    """
    def __init__(self, prompt: str, model_id: str = "gemini-pro", parameters: Dict[str, Any] = None):
        self.prompt = prompt
        self.model_id = model_id
        self.parameters = parameters if parameters is not None else {}

class LLMResponse:
    """
    Defines a generic response structure for LLM inference.
    """
    def __init__(self, generated_text: str, model_id: str = "gemini-pro", raw_response: Any = None):
        self.generated_text = generated_text
        self.model_id = model_id
        self.raw_response = raw_response

class JSONExtractionSchema:
    """
    Defines a schema for JSON extraction tasks.
    """
    def __init__(self, schema_definition: Dict[str, Any]):
        self.schema_definition = schema_definition
