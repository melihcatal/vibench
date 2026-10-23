from google.cloud import language_v1


def summarize_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    summary = " ".join(
        [
            sentence.text.content
            for sentence in response.sentences
            if sentence.sentiment.score > 0
        ]
    )
    return summary
