from typing import Dict, Any, List, Literal

class LLMRequest:
    text: str
    max_tokens: int = 1024
    temperature: float = 0.7
    
    def __init__(self, text: str, max_tokens: int = 1024, temperature: float = 0.7):
        self.text = text
        self.max_tokens = max_tokens
        self.temperature = temperature

    def to_openai_chat_completion_payload(self, model: str) -> Dict[str, Any]:
        return {
            "model": model,
            "messages": [{"role": "user", "content": self.text}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

class LLMContextRequest(LLMRequest):
    context: str

    def __init__(self, text: str, context: str, max_tokens: int = 1024, temperature: float = 0.7):
        super().__init__(text, max_tokens, temperature)
        self.context = context

    def to_openai_chat_completion_payload(self, model: str) -> Dict[str, Any]:
        prompt = f"Based on the following context, answer the question: {self.text}\n\nContext: {self.context}"
        return {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

class LLMStreamResponse:
    def __init__(self, openai_stream_chunk: Dict[str, Any]):
        self.text = openai_stream_chunk.choices[0].delta.content if openai_stream_chunk.choices and openai_stream_chunk.choices[0].delta.content else ""

class LLMResponse:
    text: str

    def __init__(self, openai_response: Dict[str, Any]):
        self.text = openai_response.choices[0].message.content if openai_response.choices else ""

class LLMJsonRequest(LLMRequest):
    json_schema: Dict[str, Any]

    def __init__(self, text: str, json_schema: Dict[str, Any], max_tokens: int = 1024, temperature: float = 0.7):
        super().__init__(text, max_tokens, temperature)
        self.json_schema = json_schema

    def to_openai_chat_completion_payload(self, model: str) -> Dict[str, Any]:
        return {
            "model": model,
            "messages": [
                {"role": "user", "content": self.text},
                {"role": "system", "content": f"Extract structured JSON from the text based on the following schema: {self.json_schema}"}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "response_format": { "type": "json_object" }
        }

