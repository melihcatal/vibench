from google.cloud import language

def archive_summary(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.summarize_text(document=document)
    return summary.summaries[0].text