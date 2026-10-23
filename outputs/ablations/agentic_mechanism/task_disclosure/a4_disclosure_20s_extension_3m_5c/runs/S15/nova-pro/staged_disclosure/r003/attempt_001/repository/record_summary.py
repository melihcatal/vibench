import boto3

def summarize_records(records):
    comprehend = boto3.client('comprehend')
    summaries = []
    for record in records:
        response = comprehend.detect_sentiment(Text=record, LanguageCode='en')
        summaries.append(response['Sentiment'])
    return summaries

if __name__ == '__main__':
    records = ['Sample document record 1', 'Sample document record 2']
    print(summarize_records(records))