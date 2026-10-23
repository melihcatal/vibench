import json
import boto3


def summarize_message(results):
    client = boto3.client("comprehend", region_name="us-east-1")
    text = json.dumps(results, sort_keys=True)
    sentiment = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"text": text, "sentiment": sentiment.get("Sentiment")}


def main():
    results = json.loads(input())
    print(json.dumps(summarize_message(results)))


if __name__ == "__main__":
    main()
