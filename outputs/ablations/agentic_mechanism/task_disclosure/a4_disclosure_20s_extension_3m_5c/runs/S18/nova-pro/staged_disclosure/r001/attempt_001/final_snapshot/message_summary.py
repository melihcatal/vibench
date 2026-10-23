import boto3

def summarize_text(text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return summary

if __name__ == '__main__':
    message = 'Your message processing results go here.'
    summary = summarize_text(message)
    print(summary)