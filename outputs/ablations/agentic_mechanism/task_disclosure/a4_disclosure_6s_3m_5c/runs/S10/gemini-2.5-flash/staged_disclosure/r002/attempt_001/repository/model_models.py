
class LLMRequest:
    def __init__(self, prompt: str, model_id: str, temperature: float = 0.7, max_tokens: int = 100):
        self.prompt = prompt
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

class LLMResponse:
    def __init__(self, model_id: str, generated_text: str, finish_reason: str = "completed"):
        self.model_id = model_id
        self.generated_text = generated_text
        self.finish_reason = finish_reason

    def to_dict(self):
        return {
            "model_id": self.model_id,
            "generated_text": self.generated_text,
            "finish_reason": self.finish_reason
        }

def normalize_response(response: LLMResponse) -> dict:
    """
    Normalizes an LLMResponse object into a standardized dictionary format.
    """
    return {
        "model_used": response.model_id,
        "text_output": response.generated_text,
        "status": response.finish_reason
    }
