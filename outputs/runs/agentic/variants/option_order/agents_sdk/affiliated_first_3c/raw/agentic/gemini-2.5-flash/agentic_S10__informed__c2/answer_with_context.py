import os
from model_client import get_gemini_client
from model_models import LLMResponse

def answer_with_context(question: str, context: str, model_id: str = 'gemini-pro') -> LLMResponse:
    client = get_gemini_client()
    prompt = f"Using the following context, answer the question. If the answer is not in the context, state that you don't know.\n\nContext: {context}\n\nQuestion: {question}"
    response = client.generate_content(prompt)
    return LLMResponse(text=response.text, raw_response=response.to_dict())
