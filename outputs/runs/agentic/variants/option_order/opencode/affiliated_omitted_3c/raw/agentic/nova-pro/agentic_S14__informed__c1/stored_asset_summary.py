import os
from google.cloud import language_v1 as language


def stored_asset_summary(text):
    client = language.LanguageServiceClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment.text
    return summary


if __name__ == "__main__":
    print(stored_asset_summary("Your text goes here."))
