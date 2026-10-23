from model_client import chat_completion
from model_models import build_system_user_messages


def summarize_text(text: str) -> str:
    system_prompt = "You are an expert at summarizing text concisely while retaining key information."
    user_prompt = f"Please summarize the following text:\\n\\n{text}"
    messages = build_system_user_messages(system_prompt, user_prompt)
    return chat_completion(messages)
