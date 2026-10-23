# appeal_translate.py
import json
from safety_models import ModerationResponse
from google.cloud import translate_v2 as translate

def translate_appeal(appeal_text: str, target_lang: str = "en") -> ModerationResponse:
    """Translate an appeal / user explanation into English for reviewer consumption.

    Uses Google Cloud Translation as the concrete provider.
    """
    client = translate.Client()
    result = client.translate(appeal_text, target_language=target_lang)
    translated = result["translatedText"]
    # Return a simple ModerationResponse wrapper containing the translation.
    return ModerationResponse(
        text=translated,
        language=target_lang,
        scores={},
        decision="TRANSLATED"
    )

if __name__ == "__main__":
    sample = "Merci beaucoup pour votre aide."
    result = translate_appeal(sample, target_lang="en")
    print(json.dumps(result.to_dict(), indent=2))
