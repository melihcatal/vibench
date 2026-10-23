import os
from google.cloud import language_v1

def check_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    attributes = {'TOXICITY': {} }
    response = client.analyze_sentiment(request={'document': document, 'attributes': attributes})
    return response.attribute_sentiments['TOXICITY'].score > 0.5

if __name__ == '__main__' :
    test_text = 'This is a test text to check for unsafe content.'
    if check_safety(test_text):
        print('Unsafe content detected')
    else:
        print('No unsafe content detected')