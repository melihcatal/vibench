import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translatedText

if __name__ == '__main__':
    # Example usage
    narration_script = 'Hello, welcome to our channel.'
    translated_script = translate_text(narration_script, 'en', 'es')
    print(translated_script)