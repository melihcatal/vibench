import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get('TranslatedText')

if __name__ == '__main__':
    image_description = 'A beautiful sunset over the mountains.'
    translated_description = translate_text(image_description, 'en', 'es')
    print(translated_description)