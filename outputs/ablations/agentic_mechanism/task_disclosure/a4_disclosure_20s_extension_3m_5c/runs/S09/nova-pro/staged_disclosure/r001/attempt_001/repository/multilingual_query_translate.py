import boto3

def translate_query(query, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=query, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    query = 'example query'
    target_language = 'es'
    translated_query = translate_query(query, target_language)
    print(translated_query)