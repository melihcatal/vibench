from model_client import chat_completion
from model_models import build_system_user_messages


def answer_with_context(question: str, context: str) -> str:
    system_prompt = "You answer questions based solely on the provided context. Be accurate and cite relevant parts if possible."
    user_prompt = f"Context: {context}\\n\\nQuestion: {question}"
    messages = build_system_user_messages(system_prompt, user_prompt)
    return chat_completion(messages)
