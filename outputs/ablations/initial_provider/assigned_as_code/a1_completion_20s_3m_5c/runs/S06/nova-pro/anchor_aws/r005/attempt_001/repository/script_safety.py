import google.auth
from google.cloud import language_v1


def check_script_safety(script):
    credentials, project = google.auth.default()
    client = language_v1.LanguageServiceClient(credentials=credentials, project=project)
    document = language_v1.Document(content=script, type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    return analysis.document_sentiment.score >= 0.5