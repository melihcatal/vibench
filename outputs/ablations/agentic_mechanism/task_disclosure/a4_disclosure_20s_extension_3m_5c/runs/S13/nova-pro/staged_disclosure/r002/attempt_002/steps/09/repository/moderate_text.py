import os
from google.cloud import language_v1

def moderate_text(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score

if __name__ == '__main__':
    user_text = input('Enter text to moderate: ')
    score = moderate_text(user_text)
    print(f'Moderation score: {score}')