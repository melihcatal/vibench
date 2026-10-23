import boto3

def summarize_message(message):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=message, LanguageCode='en')
    return summary

if __name__ == '__main__':
    message = 'Your message goes here'
    print(summarize_message(message))