import json

from messaging_client import translate_client


def translate_payload(text: str, source_language: str, target_language: str) -> dict:
    client = translate_client()
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText", ""), "source_language": source_language, "target_language": target_language}


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(translate_payload(data.get("text", ""), data.get("source_language", "en"), data.get("target_language", "es"))))


if __name__ == "__main__":
    main()
