def normalize_request(text, source_language, target_language):
    return {'Text': text, 'SourceLanguageCode': source_language, 'TargetLanguageCode': target_language}

def parse_response(response):
    return response['TranslatedText']