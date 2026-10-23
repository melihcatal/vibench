import boto3


def invoice_summary(extracted):
    comprehend = boto3.client("comprehend", region_name="us-east-1")
    text = str(extracted)
    sentiment = comprehend.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"summary": text[:280], "sentiment": sentiment.get("Sentiment")}
