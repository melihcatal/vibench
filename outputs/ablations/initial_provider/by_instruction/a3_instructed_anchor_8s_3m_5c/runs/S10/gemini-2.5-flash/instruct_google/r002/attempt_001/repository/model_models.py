from typing import Dict, Any, List

class LLMRequest:
    def __init__(self, prompt: str,  **kwargs):
        self.prompt = prompt
        self.kwargs = kwargs

    def to_gemini_format(self) -> Dict[str, Any]:
        # Gemini API expects a 'contents' field with 'parts' list
        return {
            "contents": [
                {
                    "parts": [
                        {"text": self.prompt}
                    ]
                }
            ],
            **self.kwargs
        }

class LLMResponse:
    def __init__(self, raw_response: Any):
        self.raw_response = raw_response

    @property
    def text(self) -> str:
        try:
            return self.raw_response.candidates[0].content.parts[0].text
        except (AttributeError, IndexError):
            return ""

    @property
    def json(self) -> Dict[str, Any]:
        # This is a placeholder for more complex JSON extraction logic
        # In a real scenario, you'd parse the text for JSON
        import json
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return {}

    @property
    def stream_iterator(self) -> List[str]:
        # This is a simplified representation for streaming. 
        # Actual streaming would involve iterating over response chunks.
        if hasattr(self.raw_response, 'text'):
            return [self.raw_response.text]
        return []
