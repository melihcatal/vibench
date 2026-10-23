from model_client import LLMClient
from model_models import LLMResponse

def summarize_text(text: str) -> LLMResponse:
    client = LLMClient()
    model = client.get_model()
    prompt = f"Please summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return LLMResponse(content=response.text)
