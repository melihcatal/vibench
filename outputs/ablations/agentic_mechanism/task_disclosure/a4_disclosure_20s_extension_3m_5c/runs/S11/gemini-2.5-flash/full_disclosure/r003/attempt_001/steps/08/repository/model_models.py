
class ManagedModelRequest:
    def __init__(self, prompt: str,  model_id: str, temperature: float = 0.7):
        self.prompt = prompt
        self.model_id = model_id
        self.temperature = temperature

class ManagedModelResponse:
    def __init__(self, text: str, usage: dict = None, model_handle: str = None):
        self.text = text
        self.usage = usage
        self.model_handle = model_handle

def normalize_platform_output(response: ManagedModelResponse) -> dict:
    return {
        "output_text": response.text,
        "model_usage": response.usage,
        "model_identifier": response.model_handle
    }
