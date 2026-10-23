from typing import List, Dict

from model_client import create_chat_completion
from model_models import extract_content, ChatMessages

def answer_with_context(context: str, question: str) -> str:
    messages: ChatMessages = [
        {"role": "system", "content": "Answer the question using only the provided context. If unsure, say so."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = create_chat_completion(messages)
    return extract_content(response)