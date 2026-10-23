import os
from model_client import get_llm_client
from model_models import LLMResponse

def summarize_text(text: str, model_name: str = "gpt-4o-mini") -> str:
    """Summarize long text using a hosted LLM via OpenAI provider.
    Identifies provider via import of SDK and model identifier.
    """
    client = get_llm_client(model_name)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": f"Summarize the following text in 2-3 sentences:\n{text}"}],
        temperature=0.3,
    )
    # Convert SDK response to our normalized LLMResponse wrapper
    norm_resp = LLMResponse.from_openai(response)
    return norm_resp.choices[0].message.content
