import boto3

def translate_text(text):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode='es')
    return result.TranslatedText

if __name__ == '__main__':
    text = 'Hello, world!'
    translated_text = translate_text(text)
    print(translated_text)