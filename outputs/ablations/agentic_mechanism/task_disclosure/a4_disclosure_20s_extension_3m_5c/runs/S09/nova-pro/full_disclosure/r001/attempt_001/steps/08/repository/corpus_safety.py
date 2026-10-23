import boto3

def check_corpus_text(text):
    comprehend = boto3.client('comprehend')
    try:
        response = comprehend.detect_dominant_language(Text=text)
        if response['Languages'][0]['LanguageCode']!= 'en':
            return False
    except Exception as e:
        print(f'Error: {e}')
        return False
    return True