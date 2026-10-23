import argparse
import json
import os
from dataclasses import dataclass
from typing import Iterable

from google.cloud import translate_v2 as translate


DEFAULT_PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"
DEFAULT_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


@dataclass(frozen=True)
class TranslationIssue:
    source_text: str
    translated_text: str
    issue_type: str
    severity: str
    explanation: str


def create_translation_client() -> translate.Client:
    project_id = os.environ.get(DEFAULT_PROJECT_ID_ENV)
    credentials_path = os.environ.get(DEFAULT_CREDENTIALS_ENV)
    if credentials_path and not os.environ.get(DEFAULT_CREDENTIALS_ENV):
        os.environ[DEFAULT_CREDENTIALS_ENV] = credentials_path
    if project_id and not os.environ.get(DEFAULT_PROJECT_ID_ENV):
        os.environ[DEFAULT_PROJECT_ID_ENV] = project_id
    return translate.Client(project=project_id)


def summarize_translation_quality(source_texts: Iterable[str], target_language: str, source_language: str | None = None) -> list[TranslationIssue]:
    client = create_translation_client()
    issues: list[TranslationIssue] = []
    for text in source_texts:
        result = client.translate(text, target_language=target_language, source_language=source_language)
        translated_text = result["translatedText"]
        if translated_text == text:
            issues.append(TranslationIssue(text, translated_text, "unchanged_output", "medium", "Translation matches the source text exactly."))
        if "&" in translated_text or "&amp;" in translated_text:
            issues.append(TranslationIssue(text, translated_text, "escaping_artifact", "low", "Output may contain HTML entity escaping artifacts."))
        if len(translated_text.strip()) == 0:
            issues.append(TranslationIssue(text, translated_text, "empty_output", "high", "Translation returned an empty string."))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_texts", nargs="+")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    issues = summarize_translation_quality(args.source_texts, args.target_language, args.source_language)
    print(json.dumps([issue.__dict__ for issue in issues], ensure_ascii=False))


if __name__ == "__main__":
    main()
