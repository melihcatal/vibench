import os
from model_client import get_llm_client, get_model
from model_models import build_qa_prompt

def answer_with_context(context: str, question: str, model_family: str = "mini") -> str:
    client = get_llm_client()
    model = get_model(model_family)
    prompt = build_qa_prompt(context, question)
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,
    )
    return completion.choices[0].message.content.strip()
