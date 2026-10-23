import os
from safety_models import SafetyModels


def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate appeal text using Gemini translation API.",
    Returns the translated text.",
    """
    # Placeholder implementation - replace with real Gemini SDK usage
    # from google_genai import GeminiClient
    # client = GeminiClient()
    # resp = client.translate(appeal_text, target_language=target_lang)
    # return resp.translated_text
    return f"[Translated to {target_lang}]: {appeal_text}"


if __name__ == "__main__":
    sample = "User wants to appeal a false positive moderation."
    print(translate_appeal(sample, target_lang="fr"))
