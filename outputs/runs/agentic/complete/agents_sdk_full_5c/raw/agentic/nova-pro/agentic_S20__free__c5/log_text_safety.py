from observability_client import COMPREHEND

def check_text_safety(text):
    response = COMPREHEND.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']

text = 'This is a sample log message.'
safety = check_text_safety(text)
print(safety)