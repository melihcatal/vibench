from translation_client import TranslationClient

def check_unsafe_content(text):
    client = TranslationClient()
    analysis = client.analyze_content_safety(text)
    return analysis['unsafe']