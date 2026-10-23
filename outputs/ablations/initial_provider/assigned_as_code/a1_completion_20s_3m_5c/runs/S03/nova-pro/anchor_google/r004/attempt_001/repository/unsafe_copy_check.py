from translation_client import translate_text

def unsafe_copy_check(text, target_language):
    translation = translate_text(text, target_language)
    return f'Unsafe content check for 