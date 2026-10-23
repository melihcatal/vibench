import os
from model_client import get_llm_client, get_model
from model_models import build_summarize_prompt

def summarize_text(text: str, model_family: str = "mini") -> str:
    client = get_llm_client()
    model = get_model(model_family)
    messages = [{"role": "user", "content": build_summarize_prompt(text)}]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )
    return completion.choices[0].message.content.strip()
