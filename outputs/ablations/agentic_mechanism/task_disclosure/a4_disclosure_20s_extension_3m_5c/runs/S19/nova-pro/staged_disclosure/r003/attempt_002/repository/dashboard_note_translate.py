from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Example usage
text = 'Your metric or dashboard note here'
target_language = 'es'  # Spanish
translated_text = translate_text(text, target_language)
print(translated_text)