import boto3

def translate_text(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')

# Example usage
# translated_text = translate_text('Hello, world!', 'en', 'es')