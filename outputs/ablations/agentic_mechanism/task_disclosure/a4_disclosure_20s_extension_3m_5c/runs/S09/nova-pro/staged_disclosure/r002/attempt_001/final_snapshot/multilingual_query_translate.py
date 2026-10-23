import boto3

def translate_query(query, target_language='es'):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=query, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    query = 'example query'
    translated_query = translate_query(query)
    print(f'Translated Query: {translated_query}')
