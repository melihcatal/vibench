import os
from google.cloud import language_v1


def message_summary(message):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=message, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    summary = client.summarize(document)
    return summary.summaries[0].text
