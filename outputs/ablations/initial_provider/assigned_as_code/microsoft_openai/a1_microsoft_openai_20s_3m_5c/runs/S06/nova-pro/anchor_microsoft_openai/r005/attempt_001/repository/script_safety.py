import google.cloud.language as language

def check_safety(text):
    client = language.Client()
    document = client.document_from_text(text)
    analysis = document.analyze_sentiment()
    return analysis.sentiment.score >= -0.2