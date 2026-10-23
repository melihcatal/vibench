import boto3

def translate_caption(caption, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=caption, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.translatedText

if __name__ == '__main__':
    # Example usage
    caption = 'Hello, how are you?'
    target_language = 'es'
    translated_caption = translate_caption(caption, target_language)
    print(translated_caption)