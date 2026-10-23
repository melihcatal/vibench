import json
import os
import sys

import boto3


def check_corpus_text(text: str) -> dict[str, object]:
    client = boto3.client("comprehend", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    response = client.detect_sentiment(Text=text[:5000], LanguageCode="en")
    return {"sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}


def main() -> None:
    print(json.dumps(check_corpus_text(" ".join(sys.argv[1:]))))


if __name__ == "__main__":
    main()
