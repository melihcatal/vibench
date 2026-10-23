from google.cloud import translate_v2 as translate


def translate_consent(text: str, target_language: str):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    text = "Please accept our terms and conditions"
    target_language = "es"
    print(translate_consent(text, target_language))
