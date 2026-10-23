import os
from google.cloud import language_v1

# Set up client
client = language_v1.LanguageServiceClient()


# Summarize transcription results
def archive_summary(transcript):
    document = language_v1.Document(
        content=transcript, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    summary = client.analyze_sentiment(document=document).sentences[0].text.content
    return summary


if __name__ == "__main__":
    transcript = "This is a sample transcript."
    print(archive_summary(transcript))
