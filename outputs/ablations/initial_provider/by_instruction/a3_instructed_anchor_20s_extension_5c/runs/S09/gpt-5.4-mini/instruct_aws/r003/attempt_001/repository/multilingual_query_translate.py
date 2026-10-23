import json
import sys

import boto3


def main() -> None:
    client = boto3.client("translate")
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    target = sys.argv[2] if len(sys.argv) > 2 else "en"
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target)
    sys.stdout.write(json.dumps({"translated_text": response.get("TranslatedText", text)}))


if __name__ == "__main__":
    main()
