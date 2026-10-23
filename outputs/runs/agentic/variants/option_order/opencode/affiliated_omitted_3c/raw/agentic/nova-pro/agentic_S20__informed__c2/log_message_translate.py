import os
from google.cloud import translate_v2 as translate


def translate_log_message(log_text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(log_text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    print(translate_log_message("Sample log message", "es"))
