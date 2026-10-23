from model_client import LLMClient
from model_models import LLMRequest, LLMResponse

def summarize_text(text: str) -> LLMResponse:
    """Calls a hosted LLM to summarize long text."""
    llm_client = LLMClient().get_client()
    model = llm_client.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following text concisely:\n\n{text}"

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 200,
        }
    )
    return LLMResponse(text=response.text, raw_response=response)
