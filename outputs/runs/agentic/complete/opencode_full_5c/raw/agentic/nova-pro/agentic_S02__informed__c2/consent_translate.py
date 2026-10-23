from google.cloud import translate_v2 as translate


def translate_consent(text: str, target_language: str):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    print(result["translatedText"])


if __name__ == "__main__":
    translate_consent("your-text", "es")
