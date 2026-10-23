from google.cloud import language_v1


def stored_asset_summary(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    return client.analyze_sentiment(document=document)
