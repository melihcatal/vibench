from google.cloud import translate_v2 as translate

SAMPLE_LOG = "Authentication failed due to invalid credentials."

def translate_support_log(message: str, target_language: str = "fr"):
    client = translate.Client()
    result = client.translate(
        message,
        target_language=target_language
    )
    translated_text = result["translatedText"]
    print(f"Original: {message}")
    print(f"Translated to {target_language}: {translated_text}")
    return translated_text

if __name__ == "__main__":
    translate_support_log(SAMPLE_LOG)