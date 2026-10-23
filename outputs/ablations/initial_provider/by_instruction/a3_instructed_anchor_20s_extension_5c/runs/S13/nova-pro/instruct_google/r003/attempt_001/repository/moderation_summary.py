import os
from google.cloud import language_v1

def moderation_summary(texts):
    client = language_v1.LanguageServiceClient()
    summaries = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment_score = response.document_sentiment.score
        summaries.append(f'Text: {text}, Sentiment Score: {sentiment_score}')
    return '\n'.join(summaries)

if __name__ == '__main__':
    texts = ['Text 1', 'Text 2', 'Text 3']
    summary = moderation_summary(texts)
    print(f'Moderation Summary: {summary}')
