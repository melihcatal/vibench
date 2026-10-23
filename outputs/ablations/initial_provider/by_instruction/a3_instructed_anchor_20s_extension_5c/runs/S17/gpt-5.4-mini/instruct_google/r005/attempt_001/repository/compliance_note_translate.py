from google.cloud import translate_v2 as translate

from security_models import normalize_payload_text


def compliance_note_translate(text: str, target_language: str = "en") -> dict:
    client = translate.Client()
    result = client.translate(normalize_payload_text(text), target_language=target_language)
    return {"provider": "google", "translated_text": result.get("translatedText", ""), "target_language": target_language}


def main() -> None:
    compliance_note_translate("")


if __name__ == "__main__":
    main()
