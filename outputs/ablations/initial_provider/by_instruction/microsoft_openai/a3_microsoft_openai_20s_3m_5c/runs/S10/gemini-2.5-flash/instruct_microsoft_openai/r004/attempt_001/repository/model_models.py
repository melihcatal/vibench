from typing import List, Dict, Any

# This file can be used to define custom request/response models if the default SDK models
# are not sufficient, or for normalization of data coming in/out of the LLM calls.
# For this task, we rely heavily on the OpenAI SDK's built-in models.

class LLMRequest:
    """
    A placeholder for a generic LLM request structure if custom normalization is needed.
    """
    def __init__(self, prompt: str, model: str, max_tokens: int = 150):
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens

    def to_openai_format(self) -> Dict[str, Any]:
        # Example of how a generic request might be normalized for OpenAI
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": self.prompt}],
            "max_tokens": self.max_tokens
        }

class LLMResponse:
    """
    A placeholder for a generic LLM response structure if custom post-processing/normalization is needed.
    """
    def __init__(self, raw_response: Any):
        self.raw_response = raw_response
        self.text = self._extract_text(raw_response)

    def _extract_text(self, raw_response: Any) -> str:
        # Example of how to extract text from a raw OpenAI response
        try:
            return raw_response.choices[0].message.content
        except (AttributeError, IndexError, TypeError):
            return ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "raw_response": str(self.raw_response) # Convert raw_response to string for serialization if needed
        }