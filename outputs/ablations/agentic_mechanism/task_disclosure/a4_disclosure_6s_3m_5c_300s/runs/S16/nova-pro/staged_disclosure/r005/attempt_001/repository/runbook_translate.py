import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

if __name__ == '__main__':
    runbook_notes = 'Enter your secret-rotation runbook notes here.'
    translated_notes = translate_text(runbook_notes, 'en', 'es')
    print(translated_notes)