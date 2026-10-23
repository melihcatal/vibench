from safety_client import chat_completion


def moderation_summary(text: str) -> str:
    return chat_completion(text, "Summarize moderation decisions concisely for an operations reviewer.")
