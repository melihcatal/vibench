from google.cloud import language_v1 as language

def stored_asset_summary(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document=document).document_sentiment.score
    print(f'Summary Score: {summary}')
    return summary