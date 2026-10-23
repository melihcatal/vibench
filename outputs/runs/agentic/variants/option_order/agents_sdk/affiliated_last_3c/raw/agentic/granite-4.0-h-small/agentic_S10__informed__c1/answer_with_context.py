import os
from model_client import get_llm_client
from model_models import normalize_text

def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context via a hosted LLM.
    Uses Anthropic Claude via the Anthropic SDK.
    """
    client = get_llm_client()
    system = "You are a helpful assistant. Answer the user's question using only the provided context.",
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Question: {question}\nContext:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=messages,
        temperature=0.0,
    )
    answer = response.choices[0].message.content.strip()
    return normalize_text(answer)
