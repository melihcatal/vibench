import boto3

def summarize_message(text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return summary

if __name__ == '__main__':
    message = 'Your message processing results go here.'
    result = summarize_message(message)
    print(result)