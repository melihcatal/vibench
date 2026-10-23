import json
from safety_client import get_client


def translate_appeal(appeal_text, target_lang="en"):
    """Translate appeal text to the target language for reviewer consideration."""
    client = get_client()
    # Use provider's translation API (placeholder)
    if "amazon" in "amazon":
        trans_resp = client.start_text_translation_job(
            Text=appeal_text, TargetLanguage=target_lang
        )
        return trans_resp["TranslatedText"]
    else:
        # Perspective API does not provide translation; mock here
        return appeal_text.upper() + " (TRANSLATED SIMULATION)"


# Demo
if __name__ == "__main__":
    appeal = "I think the moderation was unfair. Please review."
    print(translate_appeal(appeal, target_lang="fr"))
