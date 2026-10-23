from google.cloud import language_v1 as language


def embed_asset_metadata(metadata, config=None):
    config = config or {}
    client = language.LanguageServiceClient()
    document = language.Document()
    document.content = metadata
    document.type_ = language.Document.Type.PLAIN_TEXT
    embedding = client.analyze_sentiment(document=document).document_sentiment.score
    return {"embedding": embedding}