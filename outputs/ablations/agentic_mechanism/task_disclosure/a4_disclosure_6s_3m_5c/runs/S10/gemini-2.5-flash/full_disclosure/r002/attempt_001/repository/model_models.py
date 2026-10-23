
class ModelRequest:
    def __init__(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7):
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

class ModelResponse:
    def __init__(self, generated_text: str, model_id: str = "unknown"):
        self.generated_text = generated_text
        self.model_id = model_id

    def to_dict(self):
        return {
            "generated_text": self.generated_text,
            "model_id": self.model_id,
        }

def normalize_text(text: str) -> str:
    """
    Normalizes text by stripping whitespace and converting to lowercase.
    """
    return text.strip().lower()
