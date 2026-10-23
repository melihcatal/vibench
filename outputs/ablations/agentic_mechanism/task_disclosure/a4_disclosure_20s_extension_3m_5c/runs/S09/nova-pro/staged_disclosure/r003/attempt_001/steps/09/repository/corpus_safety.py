import boto3

def check_corpus_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    return response

if __name__ == '__main__':
    corpus_text = 'Enter corpus text here'
    result = check_corpus_text(corpus_text)
    print(result)