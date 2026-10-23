class LLMRequest:
    def __init__(self, prompt: str, model_name: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024):
        self.prompt = prompt
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

class LLMResponse:
    def __init__(self, text: str, model_name: str = "gemini-pro", finish_reason: str = None):
        self.text = text
        self.model_name = model_name
        self.finish_reason = finish_reason

class EmbeddingResult:
    def __init__(self, embedding: list[float], model_name: str):
        self.embedding = embedding
        self.model_name = model_name
