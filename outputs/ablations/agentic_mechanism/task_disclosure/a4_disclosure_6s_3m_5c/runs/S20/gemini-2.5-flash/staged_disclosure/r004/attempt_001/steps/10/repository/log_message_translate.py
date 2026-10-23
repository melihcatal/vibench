from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str) -> str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    message = "User login failed due to invalid credentials."
    translated_message = translate_log_message(message, "es")
    print(translated_message)
