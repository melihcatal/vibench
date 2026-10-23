from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def normalize_text(text):
    return text.lower().strip()


def format_response(response):
    return response["sentiment"]["document"]["label"]
