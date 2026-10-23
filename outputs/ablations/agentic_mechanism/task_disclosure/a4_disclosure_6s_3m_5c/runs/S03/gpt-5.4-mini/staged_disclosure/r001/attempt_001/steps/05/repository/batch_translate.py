import argparse
import os
from typing import Iterable

from google.cloud import translate_v2 as translate


def batch_translate_texts(texts: Iterable[str], target_language: str, source_language: str | None = None) -> list[str]:
    client = translate.Client()
    items = list(texts)
    if not items:
        return []
    results = client.translate(items, target_language=target_language, source_language=source_language)
    if isinstance(results, dict):
        results = [results]
    return [result["translatedText"] for result in results]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_language")
    parser.add_argument("texts", nargs="+")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    translated = batch_translate_texts(args.texts, args.target_language, args.source_language)
    for item in translated:
        print(item)


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        pass
    main()
