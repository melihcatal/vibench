import os
from google.cloud import language_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def embed_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    return response.document_sentiment.score


if __name__ == "__main__":
    print(embed_text("Hello, world!"))
