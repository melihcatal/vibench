import json

class BedrockInvocationRequest:
    def __init__(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7):
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature

    def to_claude_body(self):
        return json.dumps({
            "prompt": f"Human: {self.prompt}\n\nAssistant:",
            "max_tokens_to_sample": self.max_tokens,
            "temperature": self.temperature,
            "top_p": 0.9
        })

class BedrockInvocationResponse:
    def __init__(self, raw_response_body: str, model_id: str):
        self._raw_response_body = raw_response_body
        self._model_id = model_id
        self._parsed_body = json.loads(raw_response_body)

    @property
    def completion(self) -> str:
        return self._parsed_body.get("completion", "")

    @property
    def model_id_used(self) -> str:
        return self._model_id

    @property
    def full_response(self) -> dict:
        return self._parsed_body
