import boto3

def translate_note(note, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=note, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translatedText

# Example usage
note = 'This is an encryption compliance note.'
translated_note = translate_note(note, 'en', 'es')
print(translated_note)