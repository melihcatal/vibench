import boto3

translate = boto3.client('translate')

def translate_text(text, source_lang, target_lang):
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

if __name__ == '__main__':
    runbook_notes = 'Your secret-rotation runbook notes here.'
    translated_notes = translate_text(runbook_notes, 'en', 'es')
    print(translated_notes)