import sys

import boto3


def moderate_transcript(text: str):
    client = boto3.client("comprehend")
    return client.detect_sentiment(Text=text, LanguageCode="en")


if __name__ == "__main__":
    print(moderate_transcript(sys.argv[1]))
