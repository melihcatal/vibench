import os
import deepl

def translate_live_captions(caption_generator, target_lang='ES'):
    api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        raise ValueError('DEEPL_API_KEY environment variable is required.')
    translator = deepl.Translator(api_key)
    for caption in caption_generator:
        if caption.strip():
            result = translator.translate_text(caption, target_lang=target_lang)
            yield result.text
        else:
            yield caption