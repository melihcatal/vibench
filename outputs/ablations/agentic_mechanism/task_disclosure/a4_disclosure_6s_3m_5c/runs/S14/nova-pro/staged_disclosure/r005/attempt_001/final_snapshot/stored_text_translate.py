import boto3

def translate_text(text, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.get('TranslatedText')

def main():
    # Read the stored document and extract the text
    with open('stored_document.txt', 'r') as file:
        text = file.read()
    
    # Translate the text
    translated_text = translate_text(text, 'es')
    print(translated_text)

if __name__ == '__main__':
    main()