from google.cloud import translate_v2 as translate

def check_unsafe_content(text):
    client = translate.Client()
    result = client.translate(text, target_language='en')
    translated_text = result['translatedText']
    if 'unsafe' in translated_text.lower():
        return True
    return False