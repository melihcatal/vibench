import os
from model_client import get_llm_client
from model_models import sanitize_response

def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context via a hosted LLM (OpenAI GPT-3.5 Turbo).
    Returns the LLM's answer as a plain string.
    """
    client = get_llm_client()
    prompt = f"You are an assistant. Answer the question using only the provided context. Do not make up information.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:",
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    return sanitize_response(response['choices'][0]['message']['content'])
