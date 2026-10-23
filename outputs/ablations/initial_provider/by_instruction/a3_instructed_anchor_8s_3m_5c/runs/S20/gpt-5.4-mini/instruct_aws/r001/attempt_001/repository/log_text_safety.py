import boto3


def check_text(text: str) -> dict:
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"sentiment": response.get("Sentiment"), "provider": "aws-comprehend"}


if __name__ == "__main__":
    print(check_text("example"))
