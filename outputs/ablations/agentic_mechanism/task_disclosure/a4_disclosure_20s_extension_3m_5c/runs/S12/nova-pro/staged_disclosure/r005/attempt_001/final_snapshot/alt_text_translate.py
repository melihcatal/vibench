import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.translationText

if __name__ == '__main__':
    sample_text = 'A beautiful sunset over the mountains.'
    translated_text = translate_text(sample_text, 'en', 'es')
    print(f'Translated text: {translated_text}')
