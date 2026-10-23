import os
import boto3


def record_summary(document):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=document["name"], LanguageCode="en")
    return response["Sentiment"]


if __name__ == "__main__":
    example_document = {"name": "example", "value": 123}
    sentiment = record_summary(example_document)
    print(sentiment)
