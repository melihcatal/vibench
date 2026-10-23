from google.cloud import translate_v2 as translate
import os


def translate_live_caption(text, target_language="es"):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    caption = "Hello, this is a live caption."
    translated_caption = translate_live_caption(caption)
    print(f"Original: {caption}")
    print(f"Translated: {translated_caption}")
