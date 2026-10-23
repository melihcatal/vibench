from model_client import call_gemini_generate_content
from model_models import SummarizeRequest, LLMResponse


def summarize_text(text: str, model_name: str = "gemini-pro") -> LLMResponse:
    prompt = f"Summarize the following text:\n\n{text}"
    request = SummarizeRequest(prompt=prompt, model_name=model_name)
    return call_gemini_generate_content(request)
