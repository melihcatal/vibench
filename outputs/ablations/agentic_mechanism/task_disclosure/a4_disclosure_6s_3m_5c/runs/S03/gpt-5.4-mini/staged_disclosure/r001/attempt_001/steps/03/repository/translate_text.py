import argparse
import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=source_language)
    return result["translatedText"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    output = translate_text(args.text, args.target_language, args.source_language)
    print(output)


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        pass
    main()
