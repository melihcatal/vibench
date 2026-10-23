import os
from model_client import get_llm_client
from model_models import LLMResponse

def translate_text(text: str, target_lang: str = "es", model_name: str = "gpt-4o-mini") -> str:
    """Translate text to another language using a hosted LLM.
    Uses the model's translation capabilities via a user prompt.
    Identifies provider via SDK import and model identifier.
    Returns the translated string.
    """
    client = get_llm_client(model_name)
    prompt = f"Translate the following text to {target_lang} (language code): {text}"
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    norm_resp = LLMResponse.from_openai(response)
    return norm_resp.get_content()
