import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

# Example usage
translated_text = translate_text('Hello, world!', 'en', 'es')
print(translated_text)