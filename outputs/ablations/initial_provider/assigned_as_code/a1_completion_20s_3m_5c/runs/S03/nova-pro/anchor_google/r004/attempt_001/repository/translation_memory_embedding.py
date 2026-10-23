from translation_client import translate_text

def translation_memory_embedding(text, target_language):
    translation = translate_text(text, target_language)
    return f'Translation memory embedding for 