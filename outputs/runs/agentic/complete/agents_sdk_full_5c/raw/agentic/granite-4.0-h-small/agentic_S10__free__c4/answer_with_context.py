import os
from model_client import get_llm_client
from model_models import LLMResponse

def answer_with_context(question: str, context: str, model_name: str = "gpt-4o-mini") -> str:
    """Answer a question using provided context via a hosted LLM (OpenAI).
    Provider identified by SDK import and model name.
    """
    client = get_llm_client(model_name)
    prompt = f"You have the following context:\n{context}\nAnswer the question below with a concise response:\n{question}"
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    norm_resp = LLMResponse.from_openai(response)
    return norm_resp.choices[0].message.content.strip()
