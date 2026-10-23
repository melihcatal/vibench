from translation_client import client

def summarize_quality_issues(text: str) -> str:
    response = client.translations.summarize_quality_issues(text)
    return response['summary']