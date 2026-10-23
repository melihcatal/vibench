import os
from model_client import get_gemini_client
from model_models import LLMResponse

def answer_with_context(question: str, context: str) -> LLMResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Using the following context, answer the question:

Context: {context}

Question: {question}

Answer:"
    response = model.generate_content(prompt)
    return LLMResponse(text=response.text)
