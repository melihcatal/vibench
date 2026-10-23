from safety_client import chat_completion


def appeal_translate(text: str, target_language: str = "en") -> str:
    return chat_completion(text, f"Translate this moderation appeal into {target_language} while preserving meaning and tone.")
