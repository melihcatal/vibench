from model_client import get_llm_client
from model_models import build_system_user_prompt, normalize_completion

def summarize_text(text: str) -> str:
    client = get_llm_client()
    system_prompt = "You are an expert at summarizing text. Provide a concise and accurate summary."
    user_prompt = f"Summarize the following text:\n\n{text}"
    messages = build_system_user_prompt(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.3
    )
    return normalize_completion(response)