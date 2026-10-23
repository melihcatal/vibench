import boto3


def summarize_records(records):
    comprehend = boto3.client("comprehend")
    summaries = []
    for record in records:
        response = comprehend.detect_sentiment(Text=str(record), LanguageCode="en")
        summaries.append(response["Sentiment"])
    return summaries
