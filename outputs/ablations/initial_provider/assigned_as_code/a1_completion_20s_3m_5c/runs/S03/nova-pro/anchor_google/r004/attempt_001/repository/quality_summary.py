from translation_client import translate_text

def quality_summary(text, target_language):
    translation = translate_text(text, target_language)
    return f'Translation quality summary for 