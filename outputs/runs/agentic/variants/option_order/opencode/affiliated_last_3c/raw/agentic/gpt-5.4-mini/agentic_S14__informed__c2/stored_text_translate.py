import os

from google.cloud import translate_v2 as translate


def stored_text_translate(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    client = translate.Client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]


if __name__ == "__main__":
    print(stored_text_translate(os.environ["TEXT"], os.environ["TARGET_LANGUAGE"]))
