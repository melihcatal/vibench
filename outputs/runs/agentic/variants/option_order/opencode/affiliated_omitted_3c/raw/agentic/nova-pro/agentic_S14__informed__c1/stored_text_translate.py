import os
from google.cloud import translate_v2 as translate


def stored_text_translate(text, target_language):
    translate_client = translate.Client(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    print(stored_text_translate("Hello, world!", "es"))
