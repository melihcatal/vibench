from google.cloud import translate_v2 as translate


def translate_log_message(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    text = "This is a sample log message."
    target_language = "es"
    translated_text = translate_log_message(text, target_language)
    print(translated_text)
