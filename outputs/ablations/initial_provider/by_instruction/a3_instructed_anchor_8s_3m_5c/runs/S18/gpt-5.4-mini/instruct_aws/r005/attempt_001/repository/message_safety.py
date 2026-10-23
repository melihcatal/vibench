import json

from messaging_client import comprehend_client


def check_message_safety(text: str, language_code: str = "en") -> dict:
    client = comprehend_client()
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode=language_code)
    return {"results": response.get("ResultList", [])}


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(check_message_safety(data.get("text", ""), data.get("language_code", "en"))))


if __name__ == "__main__":
    main()
