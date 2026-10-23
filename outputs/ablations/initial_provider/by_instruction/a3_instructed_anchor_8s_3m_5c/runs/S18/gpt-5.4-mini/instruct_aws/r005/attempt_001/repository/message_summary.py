import json

from messaging_client import comprehend_client


def summarize_message(text: str, language_code: str = "en") -> dict:
    client = comprehend_client()
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    return {"sentiment": response.get("Sentiment", ""), "scores": response.get("SentimentScore", {})}


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(summarize_message(data.get("text", ""), data.get("language_code", "en"))))


if __name__ == "__main__":
    main()
